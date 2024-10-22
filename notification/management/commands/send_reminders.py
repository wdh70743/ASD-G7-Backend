from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from task.models import Task
from notification.models import Notification

class Command(BaseCommand):
    help = 'Send reminders for upcoming task deadlines'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        upcoming_tasks = Task.objects.filter(
            due_date__gte=now,
            due_date__lte=now + timedelta(hours=24)
        )

        for task in upcoming_tasks:
            for user in task.project.users.all():
                user_pref = user.notification_preference
                if user_pref and user_pref.receive_reminders:
                    reminder_interval = user_pref.custom_reminder_interval or 24
                    reminder_time = now + timedelta(hours=reminder_interval)

                    if now <= task.due_date <= reminder_time:
                        Notification.objects.create(
                            recipient=user,
                            message=f'Reminder: Task "{task.title}" is due in {reminder_interval} hours!',
                            notification_type='Custom Reminder',
                            related_task=task
                        )
        self.stdout.write(self.style.SUCCESS('Reminders sent successfully'))
