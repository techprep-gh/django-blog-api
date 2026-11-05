from rest_framework import serializers

from accounts.serializers import AuthorSerializer

from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class PostSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source="id", read_only=True)
    author = AuthorSerializer(read_only=True)
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all())
    tags = serializers.ListField(child=serializers.CharField(max_length=30), required=False)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "_id",
            "title",
            "content",
            "summary",
            "tags",
            "status",
            "category",
            "author",
            "comment_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_comment_count(self, post):
        return post.comments.count()

    def validate_tags(self, tags):
        return sorted({tag.strip().lower() for tag in tags if tag.strip()})
