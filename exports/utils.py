import csv
from io import StringIO
from django.http import HttpResponse

def generate_task_csv(tasks, filename="tasks_export.csv"):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["ID", "Title", "Description", "Status", "Priority", "Due Date", "Project", "Assigned To", "Created At"])

    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description,
            task.status,
            task.priority,
            task.due_date,
            task.project.name if task.project else '',
            task.assigned_to.username if task.assigned_to else '',
            task.created_at,
        ])

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
