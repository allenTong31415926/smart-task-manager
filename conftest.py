import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.db import connection
from tasks.models import Project, Task
from tags.models import Tag

User = get_user_model()

@pytest.fixture(autouse=True)
def db_setup():
    # Ensure database is properly set up
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    yield

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    # Create admin user directly without using Django's auth system
    user = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    user.set_password('adminpass123')
    user.save()
    return user

@pytest.fixture
def regular_user():
    # Create regular user directly without using Django's auth system
    user = User(
        username='user',
        email='user@example.com',
        role='user'
    )
    user.set_password('userpass123')
    user.save()
    return user

@pytest.fixture
def authenticated_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def project(regular_user):
    return Project.objects.create(
        title='Test Project',
        description='A test project',
        owner=regular_user
    )

@pytest.fixture
def task(project):
    return Task.objects.create(
        title='Test Task',
        description='A test task',
        project=project,
        owner=project.owner
    )

@pytest.fixture
def tag():
    return Tag.objects.create(name='test')