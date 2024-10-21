from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from project.models import Project
from task.models import Task

@receiver(post_save, sender=Task)
def notify_task_update(sender, instance, **kwargs):
    for user in instance.project.users.all():
        if user != instance.owner and user.notification_preference.receive_task_updates:
            Notification.objects.create(
                recipient=user,
                message=f'Task "{instance.title}" has been updated.',
                notification_type='Task Update',
                related_task=instance
            )

@receiver(post_save, sender=Project)
def notify_project_update(sender, instance, **kwargs):
    for user in instance.users.all():
        if user.notification_preference.receive_project_updates:
            Notification.objects.create(
                recipient=user,
                message=f'Project "{instance.projectname}" has been updated.',
                notification_type='Project Update',
                related_project=instance
            )