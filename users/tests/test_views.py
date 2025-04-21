import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestAuthenticationViews:
    def test_token_obtain_pair_success(self, api_client):
        # Create a user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
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
    
    def test_token_obtain_pair_invalid_credentials(self, api_client):
        # Create a user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # Try to obtain token with wrong password
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data
    
    def test_token_refresh_success(self, api_client):
        # Create a user
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()
        
        # First get a refresh token
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        refresh_token = response.data['refresh']
        
        # Then refresh it
        url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_token_refresh_invalid(self, api_client):
        url = reverse('token_refresh')
        data = {
            'refresh': 'invalid_token'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 