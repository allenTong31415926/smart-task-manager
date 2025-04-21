import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, Project
from datetime import datetime, timedelta

User = get_user_model()

@pytest.mark.django_db
class TestLoginView:
    def setup_method(self):
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')

    def test_login_get(self, client):
        response = client.get(self.login_url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'web/login.html' in [t.name for t in response.templates]

    def test_login_authenticated_redirect(self, authenticated_client):
        response = authenticated_client.get(self.login_url)
        assert response.status_code == 302
        assert response.url == self.dashboard_url

    def test_login_valid_credentials(self, client, test_user):
        response = client.post(self.login_url, {
            'username': test_user.username,
            'password': 'testpass123',
        })
        
        # Print debug information if the test fails
        if response.status_code != 302:
            print(f"\nResponse status code: {response.status_code}")
            print(f"Form errors: {response.context['form'].errors if 'form' in response.context else 'No form in context'}")
            print(f"Username used: {test_user.username}")
        
        assert response.status_code == 302, f"Expected redirect, got {response.status_code}"
        assert response.url == self.dashboard_url, f"Expected redirect to dashboard, got {response.url}"

    def test_login_invalid_credentials(self, client):
        response = client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors, "Expected form to have errors for invalid credentials"
        assert 'Please enter a correct username and password' in str(response.context['form'].errors['__all__'])

@pytest.mark.django_db
class TestDashboardView:
    def setup_method(self):
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_authenticated(self, authenticated_client, test_task, test_project):
        response = authenticated_client.get(self.dashboard_url)
        assert response.status_code == 200
        assert 'tasks' in response.context
        assert 'projects' in response.context
        assert list(response.context['tasks']) == [test_task]
        assert list(response.context['projects']) == [test_project]
        assert 'web/dashboard.html' in [t.name for t in response.templates]

    def test_dashboard_unauthenticated(self, client):
        response = client.get(self.dashboard_url)
        assert response.status_code == 302
        assert '/login/' in response.url

@pytest.mark.django_db
class TestAnalyticsView:
    def setup_method(self):
        self.analytics_url = reverse('analytics')

    def test_analytics_authenticated(self, authenticated_client, test_user, test_project):
        # Create a done task for Monday
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        Task.objects.create(
            title='Monday Task',
            status='done',
            project=test_project,
            assigned_to=test_user,
            created_at=datetime.combine(monday, datetime.min.time())
        )

        response = authenticated_client.get(self.analytics_url)
        assert response.status_code == 200
        assert 'weekly_summary' in response.context
        summary = response.context['weekly_summary']
        assert summary['Monday'] == 1
        assert summary['Tuesday'] == 0
        assert 'web/analytics.html' in [t.name for t in response.templates]

    def test_analytics_unauthenticated(self, client):
        response = client.get(self.analytics_url)
        assert response.status_code == 302
        assert '/login/' in response.url

@pytest.mark.django_db
class TestLogoutView:
    def setup_method(self):
        self.logout_url = reverse('logout')

    def test_logout(self, authenticated_client):
        response = authenticated_client.get(self.logout_url)
        assert response.status_code == 302
        assert response.url == reverse('login')