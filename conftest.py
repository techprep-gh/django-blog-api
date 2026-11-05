import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from posts.models import Category, Post


# pytest-timeout cannot see debugpy (its trace function has no module), so a paused
# breakpoint would be killed after the timeout.
def pytest_configure(config):
    import sys

    if sys.gettrace() is not None and config.pluginmanager.has_plugin("pytest_timeout"):
        config.pluginmanager.unregister(name="pytest_timeout")


@pytest.fixture
def alice(db):
    return get_user_model().objects.create_user("alice", first_name="Alice", last_name="Moreau")


@pytest.fixture
def bob(db):
    return get_user_model().objects.create_user("bob", first_name="Bob", last_name="Okafor")


@pytest.fixture
def django_category(db):
    return Category.objects.create(name="Django", slug="django")


@pytest.fixture
def react_category(db):
    return Category.objects.create(name="React", slug="react")


@pytest.fixture
def client_for():
    def make(user=None):
        client = APIClient()
        if user is not None:
            client.credentials(HTTP_X_USER_ID=str(user.id))
        return client

    return make


@pytest.fixture
def make_post(django_category):
    def make(author, title="A post", status=Post.Status.PUBLISHED, category=None, **fields):
        return Post.objects.create(
            author=author,
            category=category or django_category,
            title=title,
            content=fields.pop("content", f"Body of {title}"),
            status=status,
            **fields,
        )

    return make
