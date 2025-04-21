from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)

    def confirm_login_allowed(self, user):
        # Skip the is_active check since we don't use that field
        pass
