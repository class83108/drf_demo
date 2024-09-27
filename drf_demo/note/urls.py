from django.urls import path
from .views import workspace_list, workspace_detail, WorkspaceList, WorkspaceDetail

urlpatterns = [
    # path("workspaces/", workspace_list, name="workspace-list"),
    path("workspaces/", WorkspaceList.as_view(), name="workspace-list"),
    path("workspaces/<int:pk>/", workspace_detail, name="workspace-detail"),
]
