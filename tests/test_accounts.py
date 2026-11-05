def test_me_returns_signed_in_user(alice, client_for):
    response = client_for(alice).get("/api/me/")

    assert response.status_code == 200
    assert response.json() == {"_id": alice.id, "username": "alice", "name": "Alice Moreau"}


def test_me_requires_user_header(db, client_for):
    response = client_for().get("/api/me/")

    assert response.status_code == 401


def test_unknown_user_id_is_rejected(db, client_for):
    client = client_for()
    client.credentials(HTTP_X_USER_ID="9999")

    assert client.get("/api/me/").status_code == 401


def test_non_numeric_user_id_is_rejected(db, client_for):
    client = client_for()
    client.credentials(HTTP_X_USER_ID="alice")

    assert client.get("/api/me/").status_code == 401


def test_my_posts_requires_user_header(db, client_for):
    assert client_for().get("/api/me/posts/").status_code == 401
