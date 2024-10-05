from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WorkspaceViewSet, DocumentViewSet

router = DefaultRouter()


router.register(r"workspaces", WorkspaceViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    # path("workspaces/", workspace_list, name="workspace-list"),
    # path("workspaces/", WorkspaceList.as_view(), name="workspace-list"),
    # path("workspaces/<int:pk>/", WorkspaceDetail.as_view(), name="workspace-detail"),
    path("", include(router.urls)),
]
