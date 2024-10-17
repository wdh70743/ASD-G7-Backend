from django.db import models

# Create your models here.


PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]
STATUS_CHOICES = [
    ('Completed', 'Completed'),
    ('Not_completed', 'Not Completed'),
]


class Task(models.Model):
    owner = models.ForeignKey("users.User", related_name="owned_tasks", on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', related_name="project_tasks", on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium', verbose_name="priority")
    status = models.BooleanField(verbose_name="status", default=False)
    title = models.CharField(max_length=100, verbose_name="title")
    description = models.CharField(max_length=3000, verbose_name="description")
    start_date = models.DateTimeField(verbose_name="start_date")
    due_date = models.DateTimeField(verbose_name="due_date")
    repeat_interval = models.PositiveIntegerField(verbose_name="repeat_interval", default=0, null=True, blank=True)
    is_archived = models.BooleanField(default=False, verbose_name="is_archived")
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name="archived_at")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at", null=True)

    def __str__(self):
        return f"{self.title} by {self.owner}"


class UserTask(models.Model):
    task = models.ForeignKey("Task", related_name="user_tasks", on_delete=models.CASCADE)
    assigned_by = models.ForeignKey("users.User", related_name="tasks_assigned_by", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey("users.User", related_name="tasks_assigned_to", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at", null=True)

    def __str__(self):
        return f"{self.task} by {self.assigned_by}"


# class TaskComment(models.Model):
#     owner = models.ForeignKey("users.User", related_name="task_comments", on_delete=models.CASCADE)
#     task = models.ForeignKey("Task", related_name="comments", on_delete=models.CASCADE)
#     comment = models.CharField(max_length=3000, verbose_name="comment")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at", null=True)
#
#     def __str__(self):
#         return f"{self.owner} -> {self.comment}"


class TaskFile(models.Model):
    owner = models.ForeignKey("users.User", related_name="task_files", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", related_name="files", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=3000, verbose_name="file_name")
    file_uri = models.FileField(upload_to="task_files/", verbose_name="file_uri")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at", null=True)

    def __str__(self):
        return f"{self.owner} -> {self.file_name}"
