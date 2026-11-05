from posts.models import Post


def test_feed_lists_only_published_posts_for_anonymous_reader(alice, make_post, client_for):
    make_post(alice, title="Live")
    make_post(alice, title="Draft", status=Post.Status.DRAFT)

    response = client_for().get("/api/posts/")

    assert response.status_code == 200
    assert [post["title"] for post in response.json()] == ["Live"]


def test_feed_includes_the_readers_own_drafts(alice, bob, make_post, client_for):
    make_post(alice, title="Alice draft", status=Post.Status.DRAFT)
    make_post(bob, title="Bob draft", status=Post.Status.DRAFT)
    make_post(bob, title="Bob live")

    titles = {post["title"] for post in client_for(alice).get("/api/posts/").json()}

    assert titles == {"Alice draft", "Bob live"}


def test_feed_is_newest_first(alice, make_post, client_for):
    make_post(alice, title="First")
    make_post(alice, title="Second")

    titles = [post["title"] for post in client_for().get("/api/posts/").json()]

    assert titles == ["Second", "First"]


def test_feed_filters_by_category(alice, make_post, react_category, client_for):
    make_post(alice, title="Django post")
    make_post(alice, title="React post", category=react_category)

    response = client_for().get("/api/posts/", {"category": "react"})

    assert [post["title"] for post in response.json()] == ["React post"]


def test_post_detail_has_nested_author_and_category_slug(alice, make_post, client_for):
    post = make_post(alice, title="Hello", tags=["orm"])

    body = client_for().get(f"/api/posts/{post.id}/").json()

    assert body["_id"] == post.id
    assert body["author"] == {"_id": alice.id, "username": "alice", "name": "Alice Moreau"}
    assert body["category"] == "django"
    assert body["tags"] == ["orm"]
    assert body["comment_count"] == 0


def test_draft_detail_is_hidden_from_other_users(alice, bob, make_post, client_for):
    post = make_post(alice, status=Post.Status.DRAFT)

    assert client_for(bob).get(f"/api/posts/{post.id}/").status_code == 404
    assert client_for(alice).get(f"/api/posts/{post.id}/").status_code == 200


def test_author_can_publish_their_draft(alice, make_post, client_for):
    post = make_post(alice, status=Post.Status.DRAFT)

    response = client_for(alice).patch(f"/api/posts/{post.id}/", {"status": "published"}, format="json")

    assert response.status_code == 200
    post.refresh_from_db()
    assert post.status == Post.Status.PUBLISHED


def test_other_users_cannot_edit_a_post(alice, bob, make_post, client_for):
    post = make_post(alice, title="Original")

    response = client_for(bob).patch(f"/api/posts/{post.id}/", {"title": "Hijacked"}, format="json")

    assert response.status_code == 403
    post.refresh_from_db()
    assert post.title == "Original"


def test_author_can_delete_a_post(alice, make_post, client_for):
    post = make_post(alice)

    assert client_for(alice).delete(f"/api/posts/{post.id}/").status_code == 204
    assert not Post.objects.filter(pk=post.id).exists()


def test_anonymous_users_cannot_create_posts(django_category, client_for):
    response = client_for().post(
        "/api/posts/", {"title": "Hi", "content": "Body", "category": "django"}, format="json"
    )

    assert response.status_code == 401
    assert Post.objects.count() == 0


def test_categories_are_listed_by_name(django_category, react_category, client_for):
    response = client_for().get("/api/categories/")

    assert [category["slug"] for category in response.json()] == ["django", "react"]
