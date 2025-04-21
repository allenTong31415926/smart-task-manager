from celery import shared_task
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from .utils import generate_task_csv
from tasks.models import Task
import tempfile

@shared_task
def send_csv_export_to_user(user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    tasks = Task.objects.filter(assigned_to=user)
    
    # Generate CSV content in memory
    response = generate_task_csv(tasks)
    file_content = response.content
    
    # Create and send email with CSV attachment
    email = EmailMessage(
        subject="Your Task Export",
        body="Attached is your exported task list.",
        from_email="noreply@smarttaskmanager.com",
        to=[user.email]
    )
    email.attach(f"{user.username}_tasks.csv", file_content, 'text/csv')
    email.send()
