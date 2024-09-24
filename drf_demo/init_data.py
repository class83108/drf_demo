from django.contrib.auth import get_user_model
from note.models import Workspace, Document

User = get_user_model()

# 創建用戶
user1 = User.objects.create_user(username="alice", password="password123")
user2 = User.objects.create_user(username="bob", password="password456")

# 創建工作空間
workspace = Workspace.objects.create(name="DRF Project", owner=user1)
workspace.members.add(user1)

# 創建文檔
doc1 = Document.objects.create(
    title="DRF Serializers",
    content="Serializers in DRF convert complex data to native Python datatypes.",
    workspace=workspace,
    created_by=user1,
)

doc2 = Document.objects.create(
    title="DRF Views",
    content="DRF provides generic views for common operations.",
    workspace=workspace,
    created_by=user1,
)

doc3 = Document.objects.create(
    title="DRF Permissions",
    content="DRF offers a flexible system for access control.",
    workspace=workspace,
    created_by=user1,
)

print("Sample data created successfully!")
print(f"Users: {User.objects.all()}")
print(f"Workspace: {Workspace.objects.all()}")
print(f"Documents: {Document.objects.all()}")
