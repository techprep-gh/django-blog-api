from django.urls import path

from . import views

urlpatterns = [
    path("posts/<int:post_id>/comments/", views.PostCommentsView.as_view(), name="post-comments"),
]
