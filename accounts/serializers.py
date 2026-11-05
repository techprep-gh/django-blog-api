from django.contrib.auth import get_user_model
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source="id", read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ["_id", "username", "name"]

    def get_name(self, user):
        return user.get_full_name() or user.username
