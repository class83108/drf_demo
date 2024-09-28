from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Document, Workspace

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class BaseWorkspaceSerializer(BaseSerializer):
    owner = MemberSerializer(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Workspace
        fields = ["id", "name", "owner", "created_at"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title"]


# class WorkspaceListSerializer(BaseWorkspaceSerializer):
#     pass


class WorkspaceSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if len(data["title"]) > len(data["content"]):
            raise serializers.ValidationError("標題不能長於內容。")
        return data

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("名稱至少需要3個字符。")
        return value

    class Meta:
        model = Workspace
        fields = ["id", "name", "owner", "members"]


class WorkspaceDetailSerializer(BaseWorkspaceSerializer):
    members = MemberSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, instance):
        request = self.context.get("request")
        return request.user == instance.owner

    class Meta(BaseWorkspaceSerializer.Meta):
        fields = BaseWorkspaceSerializer.Meta.fields + [
            "members",
            "documents",
            "is_owner",
        ]


# class WorkspaceSerializer(serializers.ModelSerializer):
#     owner = MemberSerializer(read_only=True)
#     members = MemberSerializer(many=True, read_only=True)
#     documents = DocumentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Workspace
#         fields = ["id", "name", "owner", "members", "documents", "created_at"]


class WorkspaceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Workspace
        # fields = ["id", "name", "owner", "members", "created_at"]


# class DocumentSerializer(BaseSerializer):
#     class Meta(BaseSerializer.Meta):
#         model = Document
#         fields = [
#             "id",
#             "title",
#             "content",
#             "workspace",
#             "created_by",
#             "created_at",
#             "updated_at",
#         ]


# class WorkspaceSerializer(serializers.ModelSerializer):

#     # owner = serializers.StringRelatedField(read_only=True)
#     owner_name = serializers.CharField(source="owner.username", read_only=True)
#     # members = serializers.StringRelatedField(many=True, read_only=True)
#     members_name = serializers.StringRelatedField(
#         source="members", many=True, read_only=True
#     )
#     created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
#     # StringRelatedField may be used to represent the target of the relationship using its __str__ method.
#     document_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Workspace
#         fields = [
#             "id",
#             "name",
#             # "owner",
#             # "members",
#             "owner_name",
#             "members_name",
#             "created_at",
#             "document_count",
#         ]
#         read_only_fields = ["id", "created_at"]

#     def create(self, validated_data):
#         if isinstance(validated_data, list):
#             return Workspace.objects.bulk_create(validated_data)
#         return super().create(validated_data)

#     def get_document_count(self, instance):
#         return instance.documents.count()

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation["document_info"] = instance.documents.values("title")
#         return representation


# class DocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Document
#         fields = [
#             "id",
#             "title",
#             "content",
#             "workspace",
#             "created_by",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["id", "created_at", "updated_at"]
