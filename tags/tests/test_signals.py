import pytest
from django.contrib.auth import get_user_model
from tags.models import Tag
from tasks.models import Task, Project

@pytest.mark.django_db
class TestTagSignals:
    def test_auto_tag_task_on_creation(self):
        # Create a user and project first
        User = get_user_model()
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass',
            role='user'
        )
        project = Project.objects.create(name='Test Project', owner=user)
        
        # Create task with project
        task = Task.objects.create(
            title='Urgent bug fix needed',
            project=project
        )
        # Should create both 'urgent' and 'bug' tags
        assert Tag.objects.filter(name='urgent').exists()
        assert Tag.objects.filter(name='bug').exists()
        urgent_tag = Tag.objects.get(name='urgent')
        bug_tag = Tag.objects.get(name='bug')
        assert task in urgent_tag.tasks.all()
        assert task in bug_tag.tasks.all()
    
    def test_auto_tag_task_on_update(self):
        # Create a user and project first
        User = get_user_model()
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass',
            role='user'
        )
        project = Project.objects.create(name='Test Project', owner=user)
        
        # Create task with project
        task = Task.objects.create(
            title='Regular task',
            project=project
        )
        task.title = 'UI design needed for launch'
        task.save()
        # Should create 'design' and 'deploy' tags
        assert Tag.objects.filter(name='design').exists()
        assert Tag.objects.filter(name='deploy').exists()
        design_tag = Tag.objects.get(name='design')
        deploy_tag = Tag.objects.get(name='deploy')
        assert task in design_tag.tasks.all()
        assert task in deploy_tag.tasks.all() 