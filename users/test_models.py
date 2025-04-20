import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.check_password('testpass123') is True
    
    def test_create_superuser(self):
        user = User(
            username='superuser',
            email='super@example.com',
            role='admin'
        )
        user.set_password('superpass123')
        user.save()
        
        assert user.username == 'superuser'
        assert user.email == 'super@example.com'
        assert user.role == 'admin'
        assert user.check_password('superpass123') is True
    
    def test_user_str_representation(self):
        user = User(
            username='testuser',
            email='test@example.com',
            role='admin'
        )
        user.set_password('testpass123')
        user.save()
        
        assert str(user) == 'testuser (admin)' 