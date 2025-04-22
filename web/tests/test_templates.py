import pytest
from django.template.loader import render_to_string
from django.template import Context, Template
from tasks.models import Task, Project
from datetime import datetime, timedelta

@pytest.mark.django_db
class TestLoginTemplate:
    def test_login_template_with_form(self, client):
        """Test that login template renders correctly with form"""
        response = client.get('/login/')
        assert 'web/login.html' in [t.name for t in response.templates]
        
        # Check form elements
        content = response.content.decode()
        assert '<form' in content
        assert 'method="post"' in content
        assert 'name="username"' in content
        assert 'name="password"' in content
        assert 'type="submit"' in content

    def test_login_template_with_errors(self, client):
        """Test that login template shows error messages"""
        response = client.post('/login/', {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        content = response.content.decode()
        assert 'Please enter a correct username and password' in content

@pytest.mark.django_db
class TestDashboardTemplate:
    def test_dashboard_template_content(self, web_client, task, project):
        """Test that dashboard template shows tasks and projects"""
        response = web_client.get('/dashboard/')
        assert 'web/dashboard.html' in [t.name for t in response.templates]
        
        content = response.content.decode()
        # Check essential content
        assert 'Dashboard' in content
        assert 'Welcome' in content
        assert 'Logout' in content
        assert 'Your Tasks' in content
        assert 'Your Projects' in content

        # Check task and project data
        assert f'{task.title} - {task.status}' in content  # Task title and status are shown together
        assert project.name in content  # Project name is shown

@pytest.mark.django_db
class TestAnalyticsTemplate:
    def test_analytics_template_content(self, web_client, regular_user, project):
        """Test that analytics template shows task statistics"""
        # Create a done task for Monday
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        monday_datetime = datetime.combine(monday, datetime.min.time())
        
        task = Task.objects.create(
            title='Monday Task',
            description='A test task',
            status='done',
            project=project,
            assigned_to=regular_user
        )
        Task.objects.filter(pk=task.pk).update(created_at=monday_datetime)

        response = web_client.get('/analytics/')
        assert 'web/analytics.html' in [t.name for t in response.templates]
        
        content = response.content.decode()
        # Check essential content
        assert 'Weekly Task Summary' in content
        assert 'Monday' in content
        assert 'Tuesday' in content
        assert 'Wednesday' in content
        
        # Check task count
        assert 'Monday: 1 tasks' in content  # Monday's task count
        assert 'Tuesday: 0 tasks' in content  # Other days have zero tasks

    def test_analytics_template_no_tasks(self, web_client):
        """Test that analytics template handles no tasks gracefully"""
        response = web_client.get('/analytics/')
        content = response.content.decode()
        
        # Should show zeros for all days
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            assert f'{day}: 0 tasks' in content  # Check format matches template

@pytest.mark.django_db
class TestCommonElements:
    """Test common elements across templates"""
    
    def test_navigation_elements(self, web_client):
        """Test that navigation elements are present"""
        response = web_client.get('/dashboard/')
        content = response.content.decode()
        
        # Check navigation elements
        assert 'Dashboard' in content  # Page title
        assert 'Welcome, user' in content  # User welcome message
        assert '<a href="/logout/">Logout</a>' in content  # Logout link

    def test_user_welcome(self, web_client):
        """Test that user welcome message is shown"""
        response = web_client.get('/dashboard/')
        content = response.content.decode()
        assert 'Welcome' in content
        assert 'user' in content  # username from regular_user fixture 