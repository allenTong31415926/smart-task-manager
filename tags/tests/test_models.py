import pytest
from django.contrib.auth import get_user_model
from tags.models import Tag
from tasks.models import Task, Project

@pytest.mark.django_db
class TestTagModel:
    def test_tag_creation(self):
        tag = Tag.objects.create(name='test_tag')
        assert tag.name == 'test_tag'
        assert str(tag) == 'test_tag'
    
    def test_tag_unique_name(self):
        Tag.objects.create(name='test_tag')
        with pytest.raises(Exception):
            Tag.objects.create(name='test_tag')
    
    def test_tag_task_relationship(self):
        # Create a user and project first
        User = get_user_model()
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass',
            role='user'
        )
        project = Project.objects.create(name='Test Project', owner=user)
        
        # Create tag and task
        tag = Tag.objects.create(name='test_tag')
        task = Task.objects.create(
            title='Test Task',
            project=project
        )
        tag.tasks.add(task)
        assert task in tag.tasks.all()
        assert tag in task.tags.all() 