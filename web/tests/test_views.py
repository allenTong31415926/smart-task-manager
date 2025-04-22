import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task
from datetime import datetime, timedelta

User = get_user_model()

@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.url = reverse('login')

    def test_get_login_page(self, client):
        """Test that login page loads correctly"""
        response = client.get(self.url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'web/login.html' in [t.name for t in response.templates]

    def test_login_success(self, client, regular_user):
        """Test successful login with valid credentials"""
        response = client.post(self.url, {
            'username': 'user',
            'password': 'userpass123'
        })
        assert response.status_code == 302
        assert response.url == reverse('dashboard')

    def test_login_failure(self, client):
        """Test login failure with invalid credentials"""
        response = client.post(self.url, {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors
        assert 'Please enter a correct username and password' in str(response.context['form'].errors['__all__'])

    def test_already_authenticated(self, web_client):
        """Test that authenticated users are redirected to dashboard"""
        response = web_client.get(self.url)
        assert response.status_code == 302
        assert response.url == reverse('dashboard')

@pytest.mark.django_db
class TestDashboardView:
    def setup_method(self):
        self.url = reverse('dashboard')

    def test_unauthenticated_access(self, client):
        """Test that unauthenticated users are redirected to login"""
        response = client.get(self.url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_authenticated_access(self, web_client, task, project):
        """Test that authenticated users can access dashboard and see their tasks/projects"""
        response = web_client.get(self.url)
        assert response.status_code == 200
        assert 'tasks' in response.context
        assert 'projects' in response.context
        assert list(response.context['tasks']) == [task]
        assert list(response.context['projects']) == [project]
        assert 'web/dashboard.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestAnalyticsView:
    def setup_method(self):
        self.url = reverse('analytics')

    def test_unauthenticated_access(self, client):
        """Test that unauthenticated users are redirected to login"""
        response = client.get(self.url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_authenticated_access(self, web_client, regular_user, project):
        """Test that authenticated users can access analytics and see task statistics"""
        # Create a done task for Monday
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        monday_datetime = datetime.combine(monday, datetime.min.time())

        # First create the task
        task = Task.objects.create(
            title='Monday Task',
            description='A test task',
            status='done',
            project=project,
            assigned_to=regular_user
        )
        
        # Then update created_at using update() to bypass auto_now_add
        Task.objects.filter(pk=task.pk).update(created_at=monday_datetime)

        response = web_client.get(self.url)
        assert response.status_code == 200
        assert 'weekly_summary' in response.context
        summary = response.context['weekly_summary']
        assert summary['Monday'] == 1
        assert summary['Tuesday'] == 0
        assert 'web/analytics.html' in [t.name for t in response.templates]

@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.url = reverse('logout')

    def test_logout(self, web_client):
        """Test that users can logout successfully"""
        response = web_client.get(self.url)
        assert response.status_code == 302
        assert response.url == reverse('login') 