from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        """
        Override to skip is_active check since we've removed that field.
        Only check if the user exists and has a valid password.
        """
        return True

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Override authenticate to use our custom user_can_authenticate method
        """
        return super().authenticate(request, username, password, **kwargs) 