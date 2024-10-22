from django.contrib import admin
from .models import Task, UserTask, TaskFile


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'project', 'title', 'priority', 'status')


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'assigned_by', 'assigned_to', 'created_at')


# class TaskCommentAdmin(admin.ModelAdmin):
#     list_display = ('task', 'owner', 'comment', 'created_at')


class TaskFileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at')


# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(UserTask, UserTaskAdmin)
# admin.site.register(TaskComment, TaskCommentAdmin)
admin.site.register(TaskFile, TaskFileAdmin)
