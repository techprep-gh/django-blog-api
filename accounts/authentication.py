from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions


class UserIdHeaderAuthentication(authentication.BaseAuthentication):
    header = "X-User-Id"

    def authenticate(self, request):
        user_id = request.headers.get(self.header)
        if not user_id:
            return None
        User = get_user_model()
        try:
            user = User.objects.get(pk=int(user_id), is_active=True)
        except (ValueError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed("Unknown user.")
        return user, None

    def authenticate_header(self, request):
        return self.header
