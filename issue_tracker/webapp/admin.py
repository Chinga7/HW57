from django.contrib import admin
from webapp.models import Issue, Type, Status, Project

# Register your models here.
admin.site.register(Issue)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project)