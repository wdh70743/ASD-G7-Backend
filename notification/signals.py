from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import Notification
from task.models import Task
from project.models import Project


@receiver(post_save, sender=Task)
def notify_task_update(sender, instance, created, **kwargs):
    """
    Creates a notification when a task is updated (not created).
    """
    if not created:  # Only trigger on updates
        print(f"Signal triggered for Task '{instance.title}' update.")
        for user in instance.project.users.all():
            if user.notification_preference.receive_task_updates:
                Notification.objects.create(
                    recipient=user,
                    message=f'Task "{instance.title}" has been updated.',
                    notification_type='Task Update',
                    related_task=instance
                )
            else:
                print(f"User '{user.username}' does not receive task updates.")

@receiver(post_save, sender=Project)
def notify_project_update(sender, instance, created, **kwargs):
    if not created:  # Only trigger on updates
        for user in instance.users.all():
            if user.notification_preference.receive_project_updates:
                Notification.objects.create(
                    recipient=user,
                    message=f'Project "{instance.projectname}" has been updated.',
                    notification_type='Project Update',
                    related_project=instance
                )
