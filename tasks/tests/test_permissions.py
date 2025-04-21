import pytest
from django.contrib.auth import get_user_model
from tasks.models import Project, Task
from tasks.permissions import IsOwnerOrReadOnly, IsTaskAssigneeOrProjectOwner

User = get_user_model()

@pytest.mark.django_db
class TestIsOwnerOrReadOnly:
    def test_owner_can_modify(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        permission = IsOwnerOrReadOnly()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_object_permission(request, view, project) is True
    
    def test_non_owner_cannot_modify(self, regular_user):
        other_user = User.objects.create(
            username='other',
            email='other@example.com',
            role='user'
        )
        other_user.set_password('otherpass123')
        other_user.save()
        
        project = Project.objects.create(
            name='Test Project',
            owner=other_user
        )
        
        permission = IsOwnerOrReadOnly()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_object_permission(request, view, project) is False

@pytest.mark.django_db
class TestIsTaskAssigneeOrProjectOwner:
    def test_task_assignee_can_modify(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=regular_user
        )
        
        permission = IsTaskAssigneeOrProjectOwner()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_object_permission(request, view, task) is True
    
    def test_project_owner_can_modify(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        other_user = User.objects.create(
            username='other',
            email='other@example.com',
            role='user'
        )
        other_user.set_password('otherpass123')
        other_user.save()
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=other_user
        )
        
        permission = IsTaskAssigneeOrProjectOwner()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_object_permission(request, view, task) is True
    
    def test_other_user_cannot_modify(self, regular_user):
        other_user = User.objects.create(
            username='other',
            email='other@example.com',
            role='user'
        )
        other_user.set_password('otherpass123')
        other_user.save()
        
        project = Project.objects.create(
            name='Test Project',
            owner=other_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=other_user
        )
        
        permission = IsTaskAssigneeOrProjectOwner()
        request = type('Request', (), {'user': regular_user})()
        view = type('View', (), {})()
        
        assert permission.has_object_permission(request, view, task) is False 