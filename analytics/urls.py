from django.urls import path
from .views import WeeklySummaryView, TagDistributionView, ProjectProgressView

urlpatterns = [
    path('weekly-summary/', WeeklySummaryView.as_view(), name='weekly-summary'),
    path('tag-distribution/', TagDistributionView.as_view(), name='tag-distribution'),
    path('project-progress/<int:project_id>/', ProjectProgressView.as_view(), name='project-progress'),
]
