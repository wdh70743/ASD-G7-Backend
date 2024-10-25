from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('Task Update', 'Task Update'),
        ('Project Update', 'Project Update'),
        ('Reminder', 'Reminder'),
        ('Custom Reminder', 'Custom Reminder'),
        ('Task Created', 'Task Created'),
    ]

    recipient = models.ForeignKey("users.User", related_name="notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    related_task = models.ForeignKey("task.Task", null=True, blank=True, on_delete=models.CASCADE)
    related_project = models.ForeignKey("project.Project", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification for {self.recipient} - {self.notification_type}"

class NotificationPreference(models.Model):
    user = models.OneToOneField('users.User', related_name='notification_preference', on_delete=models.CASCADE)
    receive_task_updates = models.BooleanField(default=True)
    receive_project_updates = models.BooleanField(default=True)
    receive_reminders = models.BooleanField(default=True)
    custom_reminder_interval = models.IntegerField(default=24, help_text="Interval in hours for custom reminders")

    def __str__(self):
        return f"Preferences for {self.user}"