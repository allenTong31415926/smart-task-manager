import pytest
from django.urls import reverse
from rest_framework import status
from tasks.models import Project, Task
from datetime import date

@pytest.mark.django_db
class TestProjectViewSet:
    def test_list_projects(self, authenticated_client, regular_user):
        # Create some projects
        Project.objects.create(name='Project 1', owner=regular_user)
        Project.objects.create(name='Project 2', owner=regular_user)
        
        url = reverse('project-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_create_project(self, authenticated_client, regular_user):
        url = reverse('project-list')
        data = {
            'name': 'New Project',
            'description': 'New Description',
            'owner': regular_user.id
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Project.objects.count() == 1
        assert Project.objects.first().owner == regular_user
    
    def test_retrieve_project(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        url = reverse('project-detail', args=[project.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Project'
    
    def test_update_project(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        url = reverse('project-detail', args=[project.id])
        data = {'name': 'Updated Project'}
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert Project.objects.get(id=project.id).name == 'Updated Project'
    
    def test_delete_project(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        url = reverse('project-detail', args=[project.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Project.objects.count() == 0

@pytest.mark.django_db
class TestTaskViewSet:
    def test_list_tasks(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        Task.objects.create(
            title='Task 1',
            project=project,
            assigned_to=regular_user
        )
        Task.objects.create(
            title='Task 2',
            project=project,
            assigned_to=regular_user
        )
        
        url = reverse('task-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
    
    def test_create_task(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'todo',
            'priority': 'medium',
            'due_date': '2024-12-31',
            'project': project.id,
            'assigned_to': regular_user.id
        }
        
        response = authenticated_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.count() == 1
    
    def test_retrieve_task(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=regular_user
        )
        
        url = reverse('task-detail', args=[task.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Task'
    
    def test_update_task(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=regular_user
        )
        
        url = reverse('task-detail', args=[task.id])
        data = {
            'title': 'Updated Task',
            'status': 'in_progress'
        }
        
        response = authenticated_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        task = Task.objects.get(id=task.id)
        assert task.title == 'Updated Task'
        assert task.status == 'in_progress'
    
    def test_delete_task(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        task = Task.objects.create(
            title='Test Task',
            project=project,
            assigned_to=regular_user
        )
        
        url = reverse('task-detail', args=[task.id])
        response = authenticated_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0
    
    def test_list_project_tasks(self, authenticated_client, regular_user):
        project = Project.objects.create(
            name='Test Project',
            owner=regular_user
        )
        
        Task.objects.create(
            title='Task 1',
            project=project,
            assigned_to=regular_user
        )
        Task.objects.create(
            title='Task 2',
            project=project,
            assigned_to=regular_user
        )
        
        url = reverse('project-task-list', args=[project.id])
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2 