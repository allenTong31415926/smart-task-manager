from django.urls import path
from .views import ProjectExportView, UserExportView, AsyncUserExportView

urlpatterns = [
    path('project/<int:project_id>/', ProjectExportView.as_view(), name='export-project'),
    path('user/', UserExportView.as_view(), name='export-user'),
    path('user/async/', AsyncUserExportView.as_view(), name='export-user-async'),
]
