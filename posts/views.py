from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CategorySerializer, PostSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.visible_to(request.user).select_related("author", "category")
        category = request.query_params.get("category")
        if category:
            posts = posts.filter(category__slug=category)
        return Response(PostSerializer(posts, many=True).data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Post.objects.visible_to(self.request.user).select_related("author", "category")
