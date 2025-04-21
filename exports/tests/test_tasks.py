import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from tasks.models import Project, Task
from exports.tasks import send_csv_export_to_user
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestTasks:
    def setup_method(self):
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        self.user.set_password('testpass123')
        self.user.save()
        
        # Create a project
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.user
        )
        
        # Create some tasks
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

    def test_send_csv_export_to_user(self):
        # Call the task directly (not through Celery)
        send_csv_export_to_user(self.user.id)
        
        # Check that email was sent
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        
        # Check email attributes
        assert email.subject == 'Your Task Export'
        assert email.to == [self.user.email]
        assert 'Attached is your exported task list.' in email.body
        assert email.from_email == 'noreply@smarttaskmanager.com'
        
        # Check attachment
        assert len(email.attachments) == 1
        filename, content, mime_type = email.attachments[0]
        assert filename == f'{self.user.username}_tasks.csv'
        assert mime_type == 'text/csv'
        
        # Check CSV content (content is already string)
        assert 'Test Task 1' in content
        assert 'Test Task 2' in content
        assert 'high' in content
        assert 'medium' in content
        assert 'todo' in content
        assert 'in_progress' in content

    def test_send_csv_export_to_user_no_tasks(self):
        # Create user with no tasks
        user_no_tasks = User(
            username='notasks',
            email='notasks@example.com',
            role='user'
        )
        user_no_tasks.set_password('testpass123')
        user_no_tasks.save()
        
        # Call the task
        send_csv_export_to_user(user_no_tasks.id)
        
        # Check that email was still sent
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        
        # Check attachment
        assert len(email.attachments) == 1
        filename, content, mime_type = email.attachments[0]
        
        # CSV should have headers but no data (content is already string)
        lines = content.split('\n')
        assert len(lines) == 2  # Header row and empty line
        assert 'ID,Title,Description' in lines[0]
        assert lines[1] == ''

    def test_send_csv_export_to_user_invalid_user(self):
        with pytest.raises(User.DoesNotExist):
            send_csv_export_to_user(99999)  # Non-existent user ID 