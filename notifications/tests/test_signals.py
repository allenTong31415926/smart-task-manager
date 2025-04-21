import pytest
from django.apps import apps
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from notifications.signals import setup_periodic_tasks

@pytest.mark.django_db
class TestNotificationSignals:
    def setup_method(self):
        # Clean up any existing periodic tasks before each test
        PeriodicTask.objects.all().delete()
        CrontabSchedule.objects.all().delete()

    def test_setup_periodic_tasks(self):
        # Get the notifications app config
        notifications_app = apps.get_app_config('notifications')
        
        # Run the signal handler
        setup_periodic_tasks(sender=notifications_app)
        
        # Check that the daily summary task was created
        daily_task = PeriodicTask.objects.get(name='Daily Task Summary Email')
        assert daily_task.task == 'notifications.tasks.send_daily_task_summary'
        assert int(daily_task.crontab.hour) == 8
        assert int(daily_task.crontab.minute) == 0
        
        # Check that the cleanup task was created
        cleanup_task = PeriodicTask.objects.get(name='Cleanup Old Done Tasks')
        assert cleanup_task.task == 'notifications.tasks.cleanup_old_tasks'
        assert int(cleanup_task.crontab.hour) == 3
        assert int(cleanup_task.crontab.minute) == 0

    def test_setup_periodic_tasks_other_app(self):
        # Get a different app config
        tasks_app = apps.get_app_config('tasks')
        
        # Run the signal handler
        setup_periodic_tasks(sender=tasks_app)
        
        # Check that no tasks were created
        assert PeriodicTask.objects.count() == 0 