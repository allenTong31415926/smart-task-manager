import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from web.forms import LoginForm

User = get_user_model()

@pytest.mark.django_db
class TestLoginForm:
    def setup_method(self):
        self.factory = RequestFactory()

    def test_valid_login(self, regular_user):
        request = self.factory.get('/')
        form = LoginForm(request=request, data={
            'username': 'user',
            'password': 'userpass123'
        })
        assert form.is_valid()
        assert form.get_user() == regular_user

    def test_invalid_username(self):
        request = self.factory.get('/')
        form = LoginForm(request=request, data={
            'username': 'wronguser',
            'password': 'userpass123'
        })
        assert not form.is_valid()
        assert 'Please enter a correct username and password' in str(form.errors['__all__'])

    def test_invalid_password(self, regular_user):
        request = self.factory.get('/')
        form = LoginForm(request=request, data={
            'username': 'user',
            'password': 'wrongpass'
        })
        assert not form.is_valid()
        assert 'Please enter a correct username and password' in str(form.errors['__all__'])

    def test_empty_form(self):
        request = self.factory.get('/')
        form = LoginForm(request=request, data={})
        assert not form.is_valid()
        assert 'username' in form.errors
        assert 'password' in form.errors 