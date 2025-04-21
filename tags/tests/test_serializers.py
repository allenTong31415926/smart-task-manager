import pytest
from tags.models import Tag
from tags.serializers import TagSerializer

@pytest.mark.django_db
class TestTagSerializer:
    def test_tag_serialization(self):
        tag = Tag.objects.create(name='test_tag')
        serializer = TagSerializer(tag)
        data = serializer.data
        assert data['name'] == 'test_tag'
        assert 'id' in data 