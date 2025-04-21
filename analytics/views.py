from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from datetime import timedelta
from tasks.models import Project
from tasks.models import Task
from tags.models import Tag

class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        tasks = Task.objects.filter(
            assigned_to=request.user,
            status='done',
            created_at__date__range=(start_of_week, end_of_week)
        )

        summary = {day: 0 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
        for task in tasks:
            day = task.created_at.strftime('%A')  # e.g., 'Monday'
            summary[day] += 1

        return Response(summary)

class TagDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_counts = {}

        tags = Tag.objects.prefetch_related('tasks').all()
        for tag in tags:
            count = tag.tasks.filter(assigned_to=request.user).count()
            if count > 0:
                tag_counts[tag.name] = count

        return Response(tag_counts)

class ProjectProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        total = project.tasks.count()
        done = project.tasks.filter(status='done').count()
        percent = (done / total * 100) if total > 0 else 0

        return Response({
            'total': total,
            'done': done,
            'percent_done': round(percent, 1),
        })