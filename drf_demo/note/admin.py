from django.contrib import admin

# Register your models here.


from .models import Workspace, Document, WorkspaceMember

admin.site.register(Workspace)
admin.site.register(Document)
admin.site.register(WorkspaceMember)
