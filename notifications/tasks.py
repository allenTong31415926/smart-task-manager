from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from tasks.models import Task
from datetime import datetime, timedelta

@shared_task
def send_daily_task_summary():
    User = get_user_model()
    for user in User.objects.all():
        tasks = Task.objects.filter(assigned_to=user, status__in=['todo', 'in_progress'])
        summary = "\n".join([f"- {task.title} ({task.status})" for task in tasks])
        if tasks:
            send_mail(
                subject="Your Daily Task Summary",
                message=f"Hi {user.username}, here are your tasks for today:\n\n{summary}",
                from_email="noreply@smarttaskmanager.com",
                recipient_list=[user.email],
                fail_silently=True
            )

@shared_task(bind=True, max_retries=3)
def cleanup_old_tasks(self):
    try:
        threshold_date = datetime.now() - timedelta(days=30)
        deleted_count, _ = Task.objects.filter(status='done', created_at__lt=threshold_date).delete()
        return f"{deleted_count} old tasks deleted."
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
