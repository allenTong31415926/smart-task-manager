import pytest
from .models import User
from .serializers import UserSerializer

@pytest.mark.django_db
class TestUserSerializer:
    def test_serialize_user(self):
        user = User(
            username='testuser',
            email='test@example.com',
            role='admin'
        )
        user.set_password('testpass123')
        user.save()
        
        serializer = UserSerializer(user)
        data = serializer.data
        
        assert data['id'] == user.id
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert data['role'] == 'admin'
    
    def test_deserialize_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'role': 'user'
        }
        
        serializer = UserSerializer(data=data)
        assert serializer.is_valid() is True
        
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'new@example.com'
        assert user.role == 'user'
    
    def test_serializer_validation(self):
        # Test with invalid email
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'role': 'user'
        }
        
        serializer = UserSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'email' in serializer.errors