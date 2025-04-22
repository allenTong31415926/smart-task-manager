import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, Project
from notifications.tasks import send_daily_task_summary, cleanup_old_tasks

User = get_user_model()

@pytest.mark.django_db
class TestNotificationTasks:
    def test_send_daily_task_summary(self):
        # Create a user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()

        # Create a project
        project = Project.objects.create(
            name='Test Project',
            owner=user
        )

        # Create some tasks for the user
        Task.objects.create(
            title='Test Task 1',
            description='Test Description 1',
            status='todo',
            assigned_to=user,
            project=project
        )
        Task.objects.create(
            title='Test Task 2',
            description='Test Description 2',
            status='in_progress',
            assigned_to=user,
            project=project
        )

        # Run the task
        send_daily_task_summary()

        # Check that an email was sent
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Your Daily Task Summary'
        assert mail.outbox[0].to == [user.email]
        assert 'Test Task 1 (todo)' in mail.outbox[0].body
        assert 'Test Task 2 (in_progress)' in mail.outbox[0].body

    def test_send_daily_task_summary_no_tasks(self):
        # Create a user with no tasks
        user = User(
            username='testuser2',
            email='test2@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()

        # Run the task
        send_daily_task_summary()

        # Check that no email was sent
        assert len(mail.outbox) == 0

    def test_cleanup_old_tasks(self):
        # Create a user
        user = User(
            username='testuser3',
            email='test3@example.com',
            role='user'
        )
        user.set_password('testpass123')
        user.save()

        # Create a project
        project = Project.objects.create(
            name='Test Project',
            owner=user
        )

        # Create an old done task
        old_date = timezone.now() - timedelta(days=31)
        old_task = Task.objects.create(
            title='Old Done Task',
            description='Old Description',
            status='done',
            assigned_to=user,
            project=project
        )
        # Update created_at after creation
        old_task.created_at = old_date
        old_task.save(update_fields=['created_at'])

        # Create a recent done task
        recent_date = timezone.now() - timedelta(days=29)
        recent_task = Task.objects.create(
            title='Recent Done Task',
            description='Recent Description',
            status='done',
            assigned_to=user,
            project=project
        )
        # Update created_at after creation
        recent_task.created_at = recent_date
        recent_task.save(update_fields=['created_at'])

        # Run the cleanup task
        result = cleanup_old_tasks()

        # Check that only the old task was deleted
        assert Task.objects.filter(status='done').count() == 1
        assert '1 old tasks deleted' in result
        assert not Task.objects.filter(title='Old Done Task').exists()
        assert Task.objects.filter(title='Recent Done Task').exists()