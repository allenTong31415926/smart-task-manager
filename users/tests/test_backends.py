import pytest
from django.contrib.auth import get_user_model
from users.backends import CustomModelBackend

User = get_user_model()

@pytest.mark.django_db
class TestCustomModelBackend:
    def test_authenticate_success(self):
        # Create a user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # Try to authenticate
        backend = CustomModelBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username='testuser',
            password='testpass123'
        )
        
        assert authenticated_user is not None
        assert authenticated_user == user
    
    def test_authenticate_invalid_credentials(self):
        # Create a user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # Try to authenticate with wrong password
        backend = CustomModelBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username='testuser',
            password='wrongpassword'
        )
        
        assert authenticated_user is None
    
    def test_authenticate_nonexistent_user(self):
        # Try to authenticate with nonexistent user
        backend = CustomModelBackend()
        authenticated_user = backend.authenticate(
            request=None,
            username='nonexistent',
            password='testpass123'
        )
        
        assert authenticated_user is None 