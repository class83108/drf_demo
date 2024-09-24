from django.contrib import admin

# Register your models here.


from .models import Workspace, Document

admin.site.register(Workspace)
admin.site.register(Document)
