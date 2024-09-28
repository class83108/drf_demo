from rest_framework import serializers
from .models import Workspace, WorkspaceMember, Document


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = WorkspaceMember
        fields = ["user", "username", "role"]


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)
    members = WorkspaceMemberSerializer(source="memberships", many=True, read_only=True)
    user_role = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ["id", "name", "owner", "members", "user_role", "created_at"]

    def get_user_role(self, obj):
        user = self.context["request"].user
        return obj.get_user_role(user)


class DocumentSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "content",
            "workspace",
            "created_by",
            "created_at",
            "updated_at",
        ]
