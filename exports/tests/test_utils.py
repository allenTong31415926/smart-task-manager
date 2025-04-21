import pytest
from django.contrib.auth import get_user_model
from tasks.models import Project, Task
from exports.utils import generate_task_csv
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestUtils:
    def setup_method(self):
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        self.user.set_password('testpass123')
        self.user.save()
        
        # Create projects
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )
        
        self.project2 = Project.objects.create(
            name='Test Project 2',
            description='Test Description 2',
            owner=self.user
        )
        
        # Create tasks with different attributes
        self.task1 = Task.objects.create(
            title='Test Task 1',
            description='Description 1',
            status='todo',
            priority='high',
            due_date=date(2024, 12, 31),
            project=self.project,
            assigned_to=self.user
        )
        
        self.task2 = Task.objects.create(
            title='Test Task 2',
            description='Description 2',
            status='in_progress',
            priority='medium',
            project=self.project,
            assigned_to=self.user
        )
        
        # Task with different project
        self.task3 = Task.objects.create(
            title='Test Task 3',
            description='Description 3',
            status='done',
            priority='low',
            project=self.project2,
            assigned_to=self.user
        )
        
        # Task with no assigned user
        self.task4 = Task.objects.create(
            title='Test Task 4',
            description='Description 4',
            status='todo',
            priority='medium',
            project=self.project,
            assigned_to=None
        )

    def test_generate_task_csv_all_fields(self):
        tasks = Task.objects.filter(project=self.project)
        response = generate_task_csv(tasks)
        
        content = response.content.decode('utf-8').split('\n')
        
        # Check header row
        header = content[0]
        assert 'ID' in header
        assert 'Title' in header
        assert 'Description' in header
        assert 'Status' in header
        assert 'Priority' in header
        assert 'Due Date' in header
        assert 'Project' in header
        assert 'Assigned To' in header
        assert 'Created At' in header
        
        # Check task data
        task1_data = [line for line in content if 'Test Task 1' in line][0]
        assert 'high' in task1_data
        assert 'todo' in task1_data
        assert '2024-12-31' in task1_data
        assert 'Test Project' in task1_data
        assert 'testuser' in task1_data

    def test_generate_task_csv_custom_filename(self):
        tasks = Task.objects.all()
        filename = "custom_export.csv"
        response = generate_task_csv(tasks, filename=filename)
        
        assert response['Content-Disposition'] == f'attachment; filename="{filename}"'

    def test_generate_task_csv_empty_fields(self):
        tasks = [self.task3, self.task4]  # Tasks with empty assigned_to
        response = generate_task_csv(tasks)
        content = response.content.decode('utf-8').split('\n')
        
        # Find task with different project
        task3_data = [line for line in content if 'Test Task 3' in line][0]
        assert 'Test Project 2' in task3_data
        
        # Find task with no assigned user
        task4_data = [line for line in content if 'Test Task 4' in line][0]
        assert 'Test Project' in task4_data
        assert ',,' in task4_data  # Empty assigned_to field

    def test_generate_task_csv_no_tasks(self):
        tasks = Task.objects.none()
        response = generate_task_csv(tasks)
        
        content = response.content.decode('utf-8').split('\n')
        # Should have header row and empty line
        assert len(content) == 2
        assert 'ID,Title,Description' in content[0]  # Header row
        assert content[1] == ''  # Empty data row 