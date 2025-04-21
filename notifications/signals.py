from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
import json

@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    if sender.name != 'notifications':
        return

    # Daily 8 AM task summary
    schedule, _ = CrontabSchedule.objects.get_or_create(hour=8, minute=0)
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Daily Task Summary Email',
        task='notifications.tasks.send_daily_task_summary'
    )

    # Cleanup old done tasks daily at 3 AM
    cleanup_schedule, _ = CrontabSchedule.objects.get_or_create(hour=3, minute=0)
    PeriodicTask.objects.get_or_create(
        crontab=cleanup_schedule,
        name='Cleanup Old Done Tasks',
        task='notifications.tasks.cleanup_old_tasks'
    )
