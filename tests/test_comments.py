from comments.models import Comment
from posts.models import Post


def test_thread_lists_comments_oldest_first(alice, bob, make_post, client_for):
    post = make_post(alice)
    Comment.objects.create(post=post, author=bob, body="First!")
    Comment.objects.create(post=post, author=alice, body="Thanks")

    response = client_for().get(f"/api/posts/{post.id}/comments/")

    assert response.status_code == 200
    assert [(c["author"]["username"], c["body"]) for c in response.json()] == [
        ("bob", "First!"),
        ("alice", "Thanks"),
    ]


def test_thread_shows_reply_parent(alice, bob, make_post, client_for):
    post = make_post(alice)
    question = Comment.objects.create(post=post, author=bob, body="Which version?")
    Comment.objects.create(post=post, author=alice, body="4.2", parent=question)

    thread = client_for().get(f"/api/posts/{post.id}/comments/").json()

    assert thread[1]["parent"] == question.id


def test_thread_of_another_users_draft_is_hidden(alice, bob, make_post, client_for):
    post = make_post(alice, status=Post.Status.DRAFT)

    assert client_for(bob).get(f"/api/posts/{post.id}/comments/").status_code == 404


def test_post_detail_counts_comments(alice, bob, make_post, client_for):
    post = make_post(alice)
    Comment.objects.create(post=post, author=bob, body="Nice")

    assert client_for().get(f"/api/posts/{post.id}/").json()["comment_count"] == 1


def test_anonymous_users_cannot_reply(alice, make_post, client_for):
    post = make_post(alice)

    response = client_for().post(f"/api/posts/{post.id}/comments/", {"body": "Hi"}, format="json")

    assert response.status_code == 401
