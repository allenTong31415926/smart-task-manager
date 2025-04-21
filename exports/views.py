from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tasks.models import Project, Task
from .utils import generate_task_csv
from .tasks import send_csv_export_to_user

class ProjectExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=404)

        tasks = project.tasks.all()
        return generate_task_csv(tasks, filename=f"{project.name}_tasks.csv")

class UserExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        return generate_task_csv(tasks, filename=f"{request.user.username}_tasks.csv")

class AsyncUserExportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        send_csv_export_to_user.delay(request.user.id)
        return Response({"detail": "Export started. You will receive an email shortly."})