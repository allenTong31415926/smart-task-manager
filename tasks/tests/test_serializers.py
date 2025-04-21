import pytest
from django.contrib.auth import get_user_model
from tasks.models import Project, Task
from tasks.serializers import ProjectSerializer, TaskSerializer
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestProjectSerializer:
    def test_serialize_project(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=regular_user
        )
        
        serializer = ProjectSerializer(project)
        data = serializer.data
        
        assert data['id'] == project.id
        assert data['name'] == 'Test Project'
        assert data['description'] == 'Test Description'
        assert data['owner'] == regular_user.id
        assert 'tasks' in data
        assert isinstance(data['tasks'], list)
    
    def test_deserialize_project(self, regular_user):
        data = {
            'name': 'New Project',
            'description': 'New Description',
            'owner': regular_user.id
        }
        
        serializer = ProjectSerializer(data=data)
        assert serializer.is_valid() is True
        
        project = serializer.save()
        assert project.name == 'New Project'
        assert project.description == 'New Description'
        assert project.owner == regular_user

@pytest.mark.django_db
class TestTaskSerializer:
    def test_serialize_task(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='todo',
            priority='medium',
            due_date=date(2024, 12, 31),
            project=project,
            assigned_to=regular_user
        )
        
        serializer = TaskSerializer(task)
        data = serializer.data
        
        assert data['id'] == task.id
        assert data['title'] == 'Test Task'
        assert data['description'] == 'Test Description'
        assert data['status'] == 'todo'
        assert data['priority'] == 'medium'
        assert data['due_date'] == '2024-12-31'
        assert data['project'] == project.id
        assert data['assigned_to'] == regular_user.id
    
    def test_deserialize_task(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'in_progress',
            'priority': 'high',
            'due_date': '2024-12-31',
            'project': project.id,
            'assigned_to': regular_user.id
        }
        
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid() is True
        
        task = serializer.save()
        assert task.title == 'New Task'
        assert task.description == 'New Description'
        assert task.status == 'in_progress'
        assert task.priority == 'high'
        assert task.due_date == date(2024, 12, 31)
        assert task.project == project
        assert task.assigned_to == regular_user
    
    def test_serializer_validation(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        # Test with invalid status
        data = {
            'title': 'Test Task',
            'status': 'invalid_status',
            'project': project.id
        }
        
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'status' in serializer.errors
        
        # Test with invalid priority
        data = {
            'title': 'Test Task',
            'priority': 'invalid_priority',
            'project': project.id
        }
        
        serializer = TaskSerializer(data=data)
        assert serializer.is_valid() is False
        assert 'priority' in serializer.errors 