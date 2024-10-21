from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from task.models import Task
from notification.models import Notification

class Command(BaseCommand):
    help = 'Send reminders for upcoming task deadlines'

    def handle(self, *args, **kwargs):
        upcoming_tasks = Task.objects.filter(
            due_date__gte=timezone.now(),
            due_date__lte=timezone.now() + timedelta(hours=24)
        )
        for task in upcoming_tasks:
            for user in task.project.users.all():
                if user.notification_preference.receive_reminders:
                    Notification.objects.create(
                        recipient=user,
                        message=f'Reminder: Task "{task.title}" is due soon!',
                        notification_type='Reminder',
                        related_task=task
                    )
        self.stdout.write(self.style.SUCCESS('Reminders sent successfully'))
