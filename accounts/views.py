from rest_framework import generics, permissions

from posts.models import Post
from posts.serializers import PostSerializer

from .serializers import AuthorSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.owned_by(self.request.user).select_related("author", "category")
