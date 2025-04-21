import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from users.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

User = get_user_model()

@pytest.mark.django_db
class TestTokenSerializers:
    def test_custom_token_obtain_pair_serializer_success(self):
        # Create a user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # Create a request context
        factory = APIRequestFactory()
        request = factory.post('/')
        
        # Create serializer with context
        serializer = CustomTokenObtainPairSerializer(data={
            'username': 'testuser',
            'password': 'testpass123'
        }, context={'request': request})

        # Validate the serializer
        assert serializer.is_valid() is True

        # Get the validated data
        data = serializer.validated_data

        # Check that we got both tokens
        assert 'access' in data
        assert 'refresh' in data
    
    def test_custom_token_obtain_pair_serializer_invalid_credentials(self):
        # Create a user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()

        # Create a request context
        factory = APIRequestFactory()
        request = factory.post('/')

        # Create serializer with context and wrong password
        serializer = CustomTokenObtainPairSerializer(data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, context={'request': request})
        
        # Validate the serializer should fail
        assert serializer.is_valid() is False
        assert 'non_field_errors' in serializer.errors

    def test_custom_token_refresh_serializer(self):
        # Create a user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()

        # Create a request context
        factory = APIRequestFactory()
        request = factory.post('/')

        # First get a refresh token
        obtain_serializer = CustomTokenObtainPairSerializer(data={
            'username': 'testuser',
            'password': 'testpass123'
        }, context={'request': request})

        assert obtain_serializer.is_valid() is True
        refresh_token = obtain_serializer.validated_data['refresh']

        # Now use the refresh token to get a new access token
        refresh_serializer = CustomTokenRefreshSerializer(data={
            'refresh': refresh_token
        })

        assert refresh_serializer.is_valid() is True
        data = refresh_serializer.validated_data

        assert 'access' in data 