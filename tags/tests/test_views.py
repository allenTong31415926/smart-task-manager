import pytest
from django.urls import reverse
from rest_framework import status
from tags.models import Tag

@pytest.mark.django_db
class TestTagViewSet:
    def test_list_tags_unauthenticated(self, api_client):
        url = reverse('tag-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_tags_authenticated(self, authenticated_client):
        Tag.objects.create(name='test_tag')
        url = reverse('tag-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'test_tag'
    
    def test_retrieve_tag(self, authenticated_client):
        tag = Tag.objects.create(name='test_tag')
        url = reverse('tag-detail', args=[tag.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'test_tag'
    
    def test_create_tag_not_allowed(self, authenticated_client):
        """
        Test that creating tags manually is not allowed.
        
        Tags are automatically created by the system based on task titles
        through signals, rather than being manually created by users.
        The TagViewSet uses ReadOnlyModelViewSet to enforce this design.
        """
        url = reverse('tag-list')
        data = {'name': 'new_tag'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED 