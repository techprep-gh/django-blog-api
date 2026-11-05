from django.shortcuts import get_object_or_404
from rest_framework import generics

from posts.models import Post

from .models import Comment
from .serializers import CommentSerializer


class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post.objects.visible_to(self.request.user), pk=self.kwargs["post_id"])

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post()).select_related("author")

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)
