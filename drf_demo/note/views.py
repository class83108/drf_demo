from rest_framework import viewsets, permissions
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import filters
from django.contrib.auth.models import User
from .models import Workspace, Document
from .serializers import (
    WorkspaceSerializer,
    DocumentSerializer,
)
from rest_framework.authtoken.views import obtain_auth_token


class CustomPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class WorkspaceViewSet(viewsets.ModelViewSet):
    # authentication_classes = [BaseAuthentication, TokenAuthentication]
    # throttle_classes = [UserRateThrottle]
    pagination_class = PageNumberPagination
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 用戶只能看到他們是成員的工作區
        return Workspace.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        workspace.add_member(self.request.user, role="OWNER")

    def perform_destroy(self, instance):
        if instance.can_delete(self.request.user):
            instance.delete()
        else:
            raise permissions.PermissionDenied(
                "You don't have permission to delete this workspace."
            )

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        workspace = self.get_object()
        if not workspace.can_manage_members(request.user):
            raise permissions.PermissionDenied(
                "You don't have permission to add members."
            )
        user_id = request.data.get("user_id")
        role = request.data.get("role", "READER")
        user = User.objects.get(pk=user_id)

        workspace.add_member(user, role)
        return Response({"status": "member added"})

    @action(detail=True, methods=["post"])
    def change_member_role(self, request, pk=None):
        workspace = self.get_object()
        if not workspace.can_manage_members(request.user):
            raise permissions.PermissionDenied(
                "You don't have permission to change member roles."
            )

        user_id = request.data.get("user_id")
        new_role = request.data.get("role")
        user = User.objects.get(pk=user_id)

        workspace.change_member_role(user, new_role)
        return Response({"status": "member role changed"})

    @action(detail=True, methods=["post"])
    def remove_member(self, request, pk=None):
        workspace = self.get_object()
        if not workspace.can_manage_members(request.user):
            raise permissions.PermissionDenied(
                "You don't have permission to remove members."
            )

        user_id = request.data.get("user_id")
        user = User.objects.get(pk=user_id)

        workspace.remove_member(user)
        return Response({"status": "member removed"})


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["workspace__owner__username"]
    ordering_fields = ["created_at", "updated_at", "id"]

    # def get_queryset(self):
    #     # 用戶只能看到他們有權限的工作區中的文檔
    #     return Document.objects.filter(workspace__memberships__user=self.request.user)

    def perform_create(self, serializer):
        workspace = serializer.validated_data["workspace"]
        if workspace.can_edit(self.request.user):
            serializer.save(created_by=self.request.user)
        else:
            raise permissions.PermissionDenied(
                "You don't have permission to create documents in this workspace."
            )

    def perform_update(self, serializer):
        if serializer.instance.workspace.can_edit(self.request.user):
            serializer.save()
        else:
            raise permissions.PermissionDenied(
                "You don't have permission to edit this document."
            )

    def perform_destroy(self, instance):
        if instance.workspace.can_edit(self.request.user):
            instance.delete()
        else:
            raise permissions.PermissionDenied(
                "You don't have permission to delete this document."
            )
