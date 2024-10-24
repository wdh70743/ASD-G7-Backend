from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from task.models import Task
from project.models import Project
from notification.models import Notification


class Command(BaseCommand):
    help = 'Send reminders for upcoming task and project deadlines'

    def handle(self, *args, **kwargs):
        now = timezone.now()

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

        # Handle upcoming projects
        upcoming_projects = Project.objects.filter(
            end_date__gte=now.date(),
            end_date__lte=(now + timedelta(days=1)).date()
        )

        for project in upcoming_projects:
            # Convert project end date to a timezone-aware datetime
            project_end_datetime = timezone.make_aware(
                datetime.combine(project.end_date, datetime.min.time())
            )

            for user in project.users.all():
                if now <= project_end_datetime <= (now + timedelta(hours=24)):
                    Notification.objects.create(
                        recipient=user,
                        message=f'Reminder: Project \"{project.projectname}\" is ending soon!',
                        notification_type = 'Custom Reminder',
                        related_project = project
                    )
        self.stdout.write(self.style.SUCCESS('Reminders sent successfully'))