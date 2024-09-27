from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Document, Workspace

User = get_user_model()


# class WorkspaceSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=100)
#     owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
#     created_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         members = validated_data.pop("members", [])
#         workspace = Workspace.objects.create(**validated_data)
#         workspace.members.set(members)
#         return workspace

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.owner = validated_data.get("owner", instance.owner)

#         members = validated_data.get("members")
#         if members is not None:
#             instance.members.set(members)

#         instance.save()
#         return instance


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "owner",
            "members",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        if isinstance(validated_data, list):
            return Workspace.objects.bulk_create(validated_data)
        return super().create(validated_data)

    # def create(self, validated_data):
    #     members = validated_data.pop("members", [])
    #     workspace = Workspace.objects.create(**validated_data)
    #     workspace.members.set(members)
    #     return workspace

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.owner = validated_data.get("owner", instance.owner)

    #     members = validated_data.get("members")
    #     if members is not None:
    #         instance.members.set(members)

    #     instance.save()
    #     return instance


class DocumentSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "created_at", "updated_at"]

    # def create(self, validated_data):
    #     return Document.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.content = validated_data.get("content", instance.content)
    #     instance.workspace = validated_data.get("workspace", instance.workspace)
    #     instance.save()
    #     return instance
