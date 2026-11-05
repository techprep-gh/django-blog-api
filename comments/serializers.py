from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accounts.serializers import AuthorSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source="id", read_only=True)
    author = AuthorSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ["_id", "body", "parent", "author", "created_at"]
        read_only_fields = ["created_at"]

    def validate_body(self, body):
        body = body.strip()
        if not body:
            raise serializers.ValidationError("Reply cannot be empty.")
        return body

    def create(self, validated_data):
        comment = Comment(**validated_data)
        try:
            comment.full_clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.message_dict)
        comment.save()
        return comment
