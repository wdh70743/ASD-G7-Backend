from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'project', 'title', 'priority', 'status')


# Register your models here.
admin.site.register(Task, TaskAdmin)