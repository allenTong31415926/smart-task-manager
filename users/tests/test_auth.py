import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

@pytest.mark.django_db
class TestAuthentication:
    def test_obtain_token_success(self, api_client):
        # Create user directly with only the fields that exist in our model
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # Verify user was created
        assert User.objects.filter(username='testuser').exists()
        
        # Verify password
        assert user.check_password('testpass123')
        
        # Try to authenticate
        authenticated_user = authenticate(username='testuser', password='testpass123')
        assert authenticated_user is not None
        
        # Try to obtain token
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_obtain_token_invalid_credentials(self, api_client):
        """Test token obtain with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data
        assert response.data['non_field_errors'][0] == 'Unable to log in with provided credentials.'
    
    def test_refresh_token_success(self, api_client):
        # Create user and get token
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        refresh_token = response.data['refresh']
        
        # Then refresh it
        url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_refresh_token_invalid(self, api_client):
        url = reverse('token_refresh')
        data = {
            'refresh': 'invalid_token'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 