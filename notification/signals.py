from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, NotificationPreference
from task.models import Task
from project.models import Project
from users.models import User


@receiver(post_save, sender=Task)
def notify_task_creation_or_update(sender, instance, created, **kwargs):
    """
    Creates a notification when a task is created or updated.
    """
    # Get users associated with the project
    users = instance.project.users.all()

    if created:
        # Trigger notification on task creation
        for user in users:
            Notification.objects.create(
                recipient=user,
                message=f'A new task "{instance.title}" has been created.',
                notification_type='Task Created',
                related_task=instance
            )
    else:
        # Trigger notification on task update
        for user in users:
            if user.notification_preference.receive_task_updates:
                Notification.objects.create(
                    recipient=user,
                    message=f'Task "{instance.title}" has been updated.',
                    notification_type='Task Created',
                    related_task=instance
                )
            else:
                print(f"User '{user.username}' does not receive task updates.")

@receiver(post_save, sender=Project)
def notify_project_update(sender, instance, created, **kwargs):
    if not created:  # Only trigger on updates
        for user in instance.users.all():
            print(user.email)
            if hasattr(user,
                       'notification_preference') and user.notification_preference and user.notification_preference.receive_project_updates:
                Notification.objects.create(
                    recipient=user,
                    message=f'Project "{instance.projectname}" has been updated.',
                    notification_type='Project Update',
                    related_project=instance
                )
@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """
    Signal to automatically create NotificationPreference when a new user is created
    """
    if created:  # 새로운 유저가 생성될 때만
        NotificationPreference.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_notification_preferences(sender, instance, **kwargs):
    """
    Signal to save NotificationPreference if User is updated
    """
    try:
        instance.notification_preference.save()
    except NotificationPreference.DoesNotExist:
        NotificationPreference.objects.create(user=instance)
