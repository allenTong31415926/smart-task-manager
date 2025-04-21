import pytest
from django.template.loader import render_to_string
from tasks.models import Task
from web.forms import LoginForm

@pytest.mark.django_db
class TestLoginTemplate:
    def test_login_template_empty_form(self):
        form = LoginForm()
        html = render_to_string('web/login.html', {'form': form})
        
        # Check basic structure
        assert '<form' in html
        assert 'method="post"' in html
        assert 'csrfmiddlewaretoken' in html
        assert '<button type="submit">Login</button>' in html
        
        # Check form fields
        assert 'id="id_username"' in html
        assert 'id="id_password"' in html

    def test_login_template_with_errors(self):
        form = LoginForm(data={'username': '', 'password': ''})
        form.is_valid()  # Trigger validation to get errors
        html = render_to_string('web/login.html', {'form': form})
        
        # Check error messages
        assert 'This field is required.' in html

@pytest.mark.django_db
class TestDashboardTemplate:
    def test_dashboard_template_with_data(self, test_user, test_task, test_project):
        context = {
            'tasks': Task.objects.filter(assigned_to=test_user),
            'projects': [test_project]
        }
        html = render_to_string('web/dashboard.html', context)
        
        # Check if project and task data is displayed
        assert 'Test Project' in html
        assert 'Test Task' in html
        assert 'todo' in html
        assert 'high' in html

    def test_dashboard_template_no_data(self):
        context = {
            'tasks': Task.objects.none(),
            'projects': []
        }
        html = render_to_string('web/dashboard.html', context)
        
        # Check empty state handling
        assert 'No tasks found' in html
        assert 'No projects found' in html

@pytest.mark.django_db
class TestAnalyticsTemplate:
    def test_analytics_template_with_data(self):
        weekly_summary = {
            'Monday': 2,
            'Tuesday': 1,
            'Wednesday': 0,
            'Thursday': 3,
            'Friday': 1,
            'Saturday': 0,
            'Sunday': 0
        }
        html = render_to_string('web/analytics.html', {'weekly_summary': weekly_summary})
        
        # Check if all days are displayed
        for day in weekly_summary:
            assert day in html
            assert str(weekly_summary[day]) in html

    def test_analytics_template_no_data(self):
        weekly_summary = {
            'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,
            'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0
        }
        html = render_to_string('web/analytics.html', {'weekly_summary': weekly_summary})
        
        # Check empty state handling
        assert 'No tasks completed this week' in html 