import pytest
from django.contrib.auth import get_user_model
from tasks.models import Project, Task
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=regular_user
        )
        
        assert project.name == 'Test Project'
        assert project.description == 'Test Description'
        assert project.owner == regular_user
        assert project.created_at is not None
        assert project.updated_at is not None
    
    def test_project_str_representation(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        assert str(project) == 'Test Project'

@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self, regular_user):
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
        
        assert task.title == 'Test Task'
        assert task.description == 'Test Description'
        assert task.status == 'todo'
        assert task.priority == 'medium'
        assert task.due_date == date(2024, 12, 31)
        assert task.project == project
        assert task.assigned_to == regular_user
        assert task.created_at is not None
        assert task.updated_at is not None
    
    def test_task_str_representation(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project
        )
        assert str(task) == 'Test Task'
    
    def test_task_default_values(self, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project
        )
        
        assert task.status == 'todo'
        assert task.priority == 'medium'
        assert task.due_date is None
        assert task.assigned_to is None 