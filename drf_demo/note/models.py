from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_workspaces"
    )
    # members = models.ManyToManyField(User, related_name="workspaces")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_user_role(self, user):
        """
        Return the role of the user in the workspace.
        """
        if user == self.owner:
            return "OWNER"
        membership = self.memberships.filter(user=user).first()
        return membership.role if membership else None

    def can_read(self, user):
        return self.get_user_role(user) in ["OWNER", "EDITOR", "READER"]

    def can_edit(self, user):
        return self.get_user_role(user) in ["OWNER", "EDITOR"]

    def can_delete(self, user):
        return self.get_user_role(user) == "OWNER"

    def can_manage_members(self, user):
        return self.get_user_role(user) == "OWNER"

    def add_member(self, user, role="READER"):
        """
        Add a user to the workspace with the given role.
        """
        if role not in ["OWNER", "EDITOR", "READER"]:
            raise ValueError("Invalid role")
        WorkspaceMember.objects.create(workspace=self, user=user, role=role)

    def remove_member(self, user):
        self.memberships.filter(user=user).delete()

    def change_member_role(self, user, new_role):
        if new_role not in ["EDITOR", "READER"]:

            raise ValueError("Invalid role")
        membership = self.memberships.get(user=user)
        membership.role = new_role
        membership.save()


class WorkspaceMember(models.Model):
    ROLE_CHOICES = (
        ("OWNER", "Owner"),
        ("EDITOR", "Editor"),
        ("READER", "Reader"),
    )

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workspace_memberships"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="READER")

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name} ({self.role})"


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="documents"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_documents"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
