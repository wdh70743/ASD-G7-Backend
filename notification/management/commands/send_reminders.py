from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from task.models import Task
from project.models import Project
from notification.models import Notification
from django.db import transaction


class Command(BaseCommand):
    help = 'Send reminders for upcoming task and project deadlines'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        self.stdout.write(f"Starting cron job for sending reminders at {now}.")

        with transaction.atomic():
            # Handle upcoming tasks
            upcoming_tasks = Task.objects.filter(
                due_date__gte=now,
                due_date__lte=now + timedelta(hours=24)
            )

            for task in upcoming_tasks:
                for user in task.project.users.all():
                    Notification.objects.create(
                        recipient=user,
                        message=f'Reminder: Task "{task.title}" is due soon!',
                        notification_type='Custom Reminder',
                        related_task=task
                    )
                    self.stdout.write(f"Created reminder for user {user.username} about task '{task.title}'.")

            # Handle projects ending within 24 hours
            upcoming_projects = Project.objects.filter(
                end_date__gte=now.date(),
                end_date__lte=(now + timedelta(days=1)).date()
            )

            for project in upcoming_projects:
                self.stdout.write(f"Checking project '{project.projectname}' ending on {project.end_date}")

                for user in project.users.all():
                    Notification.objects.create(
                        recipient=user,
                        message=f'Reminder: Project \"{project.projectname}\" is ending soon!',
                        notification_type='Custom Reminder',
                        related_project=project
                    )
                    self.stdout.write(
                        f"Created reminder for user {user.username} about project '{project.projectname}'."
                    )

        self.stdout.write(self.style.SUCCESS('Reminders sent successfully'))
