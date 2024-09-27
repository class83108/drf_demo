from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    workspace_list,
    workspace_detail,
    WorkspaceList,
    WorkspaceDetail,
    WorkspaceViewSet,
)


router = DefaultRouter()


router.register(r"workspaces", WorkspaceViewSet)

urlpatterns = [
    # path("workspaces/", workspace_list, name="workspace-list"),
    # path("workspaces/", WorkspaceList.as_view(), name="workspace-list"),
    # path("workspaces/<int:pk>/", workspace_detail, name="workspace-detail"),
    path("", include(router.urls)),
]
