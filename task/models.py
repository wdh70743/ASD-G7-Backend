from django.db import models


# Create your models here.

class Task(models.Model):
    owner = models.ForeignKey("users.User", related_name="user", on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', related_name="project", on_delete=models.CASCADE)
    priority = models.ForeignKey('project.Priority', related_name="project", on_delete=models.CASCADE)
    status = models.ForeignKey('project.Status', related_name="project", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="title")
    description = models.CharField(max_length=3000, verbose_name="description")
    start_date = models.DateTimeField(verbose_name="start_date")
    due_date = models.DateTimeField(verbose_name="due_date")
    repeat_interval = models.PositiveIntegerField(verbose_name="repeat_interval")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="created_at", null=True)


class UserTask(models.Model):
    task = models.ForeignKey("Task", related_name="task", on_delete=models.CASCADE)
    assigned_by = models.ForeignKey("users.User", related_name="assigned_by", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey("users.User", related_name="assigned_to", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="created_at", null=True)


class TaskComment(models.Model):
    task = models.ForeignKey("Task", related_name="task", on_delete=models.CASCADE)
    comment = models.CharField(max_length=3000, verbose_name="comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="created_at", null=True)


class TaskFile(models.Model):
    owner = models.ForeignKey("users.User", related_name="user", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", related_name="task", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=3000, verbose_name="comment")
    file_uri = models.FileField(upload_to="images/", verbose_name="file_uri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="created_at", null=True)
