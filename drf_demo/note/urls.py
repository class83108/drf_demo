from django.urls import path
from .views import workspace_list, workspace_detail

urlpatterns = [
    path("workspaces/", workspace_list, name="workspace-list"),
    path("workspaces/<int:pk>/", workspace_detail, name="workspace-detail"),
]
