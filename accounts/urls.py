from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.MeView.as_view(), name="me"),
    path("me/posts/", views.MyPostsView.as_view(), name="my-posts"),
]
