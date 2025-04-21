import pytest
from django.urls import reverse
from rest_framework import status
from django.utils.timezone import now, make_aware
from datetime import timedelta, datetime
from tasks.models import Project, Task
from tags.models import Tag

@pytest.mark.django_db
class TestWeeklySummaryView:
    def test_weekly_summary_unauthenticated(self, api_client):
        url = reverse('weekly-summary')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_weekly_summary_empty(self, authenticated_client, regular_user):
        url = reverse('weekly-summary')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert all(count == 0 for count in response.data.values())

    def test_weekly_summary_with_tasks(self, authenticated_client, regular_user):
        # Create tasks for different days of the week
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        # Create a task for Monday
        monday_task = Task.objects.create(
            title='Monday Task',
            project=Project.objects.create(name='Test Project', owner=regular_user),
            assigned_to=regular_user,
            status='done'
        )
        # Update the created_at field after creation
        monday_date = start_of_week + timedelta(days=0)  # Monday
        monday_datetime = make_aware(datetime.combine(monday_date, datetime.min.time()))
        monday_task.created_at = monday_datetime
        monday_task.save(update_fields=['created_at'])
        
        # Create a task for Wednesday
        wednesday_task = Task.objects.create(
            title='Wednesday Task',
            project=Project.objects.create(name='Test Project 2', owner=regular_user),
            assigned_to=regular_user,
            status='done'
        )
        # Update the created_at field after creation
        wednesday_date = start_of_week + timedelta(days=2)  # Wednesday
        wednesday_datetime = make_aware(datetime.combine(wednesday_date, datetime.min.time()))
        wednesday_task.created_at = wednesday_datetime
        wednesday_task.save(update_fields=['created_at'])

        url = reverse('weekly-summary')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['Monday'] == 1
        assert response.data['Tuesday'] == 0
        assert response.data['Wednesday'] == 1
        assert response.data['Thursday'] == 0
        assert response.data['Friday'] == 0
        assert response.data['Saturday'] == 0
        assert response.data['Sunday'] == 0

@pytest.mark.django_db
class TestTagDistributionView:
    def test_tag_distribution_unauthenticated(self, api_client):
        url = reverse('tag-distribution')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_tag_distribution_empty(self, authenticated_client, regular_user):
        url = reverse('tag-distribution')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {}

    def test_tag_distribution_with_tasks(self, authenticated_client, regular_user):
        # Create tags and tasks
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        
        project = Project.objects.create(name='Test Project', owner=regular_user)
        
        # Create tasks with tags
        task1 = Task.objects.create(
            title='Task 1',
            project=project,
            assigned_to=regular_user
        )
        task1.tags.add(tag1)
        
        task2 = Task.objects.create(
            title='Task 2',
            project=project,
            assigned_to=regular_user
        )
        task2.tags.add(tag1)
        task2.tags.add(tag2)

        url = reverse('tag-distribution')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['tag1'] == 2
        assert response.data['tag2'] == 1

@pytest.mark.django_db
class TestProjectProgressView:
    def test_project_progress_unauthenticated(self, api_client):
        url = reverse('project-progress', args=[1])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_progress_not_found(self, authenticated_client, regular_user):
        url = reverse('project-progress', args=[999])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == 'Not found.'

    def test_project_progress_empty(self, authenticated_client, regular_user):
        project = Project.objects.create(name='Test Project', owner=regular_user)
        
        url = reverse('project-progress', args=[project.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total'] == 0
        assert response.data['done'] == 0
        assert response.data['percent_done'] == 0

    def test_project_progress_with_tasks(self, authenticated_client, regular_user):
        project = Project.objects.create(name='Test Project', owner=regular_user)
        
        # Create tasks with different statuses
        Task.objects.create(
            title='Done Task',
            project=project,
            assigned_to=regular_user,
            status='done'
        )
        Task.objects.create(
            title='In Progress Task',
            project=project,
            assigned_to=regular_user,
            status='in_progress'
        )
        Task.objects.create(
            title='Done Task 2',
            project=project,
            assigned_to=regular_user,
            status='done'
        )

        url = reverse('project-progress', args=[project.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total'] == 3
        assert response.data['done'] == 2
        assert response.data['percent_done'] == 66.7 