import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from rest_framework.test import APIClient
from tasks.models import Project, Task
from exports.tasks import send_csv_export_to_user
from datetime import date

User = get_user_model()

@pytest.mark.django_db
class TestExportViews:
    def setup_method(self):
        # Create test client
        self.client = APIClient()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        self.user.set_password('testpass123')
        self.user.save()
        
        # Create another user for testing permissions
        self.other_user = User(
            username='otheruser',
            email='other@example.com',
            role='user'
        )
        self.other_user.set_password('testpass123')
        self.other_user.save()
        
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

    def test_project_export_authenticated(self):
        # Login
        self.client.force_authenticate(user=self.user)
        
        # Make request
        response = self.client.get(f'/exports/project/{self.project.id}/')
        
        # Check response
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert response['Content-Disposition'] == f'attachment; filename="{self.project.name}_tasks.csv"'
        
        # Check CSV content
        content = response.content.decode()  # Django test client returns bytes, so we need to decode
        assert 'Test Task 1' in content
        assert 'Test Task 2' in content
        assert 'high' in content
        assert 'medium' in content

    def test_project_export_unauthenticated(self):
        response = self.client.get(f'/exports/project/{self.project.id}/')
        assert response.status_code == 401

    def test_project_export_wrong_user(self):
        # Login as other user
        self.client.force_authenticate(user=self.other_user)
        
        # Try to export project owned by self.user
        response = self.client.get(f'/exports/project/{self.project.id}/')
        assert response.status_code == 404

    def test_project_export_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/exports/project/99999/')
        assert response.status_code == 404

    def test_user_export_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/exports/user/')
        
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        assert response['Content-Disposition'] == f'attachment; filename="{self.user.username}_tasks.csv"'
        
        content = response.content.decode()  # Django test client returns bytes, so we need to decode
        assert 'Test Task 1' in content
        assert 'Test Task 2' in content

    def test_user_export_unauthenticated(self):
        response = self.client.get('/exports/user/')
        assert response.status_code == 401

    def test_async_user_export_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/exports/user/async/')
        
        assert response.status_code == 200
        assert response.data['detail'] == 'Export started. You will receive an email shortly.'
        
        # Execute the Celery task directly
        send_csv_export_to_user(self.user.id)
        
        # Now check that email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Your Task Export'
        assert mail.outbox[0].to == [self.user.email]
        assert len(mail.outbox[0].attachments) == 1
        assert f'{self.user.username}_tasks.csv' in mail.outbox[0].attachments[0]

    def test_async_user_export_unauthenticated(self):
        response = self.client.post('/exports/user/async/')
        assert response.status_code == 401 