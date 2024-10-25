from django.db.models.signals import post_save
from django.test import TransactionTestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from notification.models import Notification, NotificationPreference
from task.models import Task
from users.models import User
from project.models import Project
from datetime import timedelta
from django.core.management import call_command
from django.db import connection


class NotificationTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        # Set up test users
        self.user1 = User.objects.create(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create(username='user2', email='user2@example.com', password='password2')

        # Set up notification preferences
        NotificationPreference.objects.create(
            user=self.user1,
            receive_task_updates=True,
            receive_project_updates=True,
            receive_reminders=True,
            custom_reminder_interval=12
        )

        NotificationPreference.objects.create(
            user=self.user2,
            receive_task_updates=False,
            receive_project_updates=True,
            receive_reminders=True,
            custom_reminder_interval=6
        )

        # Set up project and task
        self.project = Project.objects.create(
            owner=self.user1,
            projectname='Test Project',
            description='A test project',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.project.users.add(self.user1, self.user2)

        self.task = Task.objects.create(
            owner=self.user1,
            project=self.project,
            title='Test Task',
            description='A test task',
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(hours=6)
        )

        self.client = Client()

    def test_automatic_task_creation_notification(self):
        """Test that a notification is created when a new task is created."""
        new_task = Task.objects.create(
            owner=self.user1,
            project=self.project,
            title='New Task',
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=1)
        )

        task_creation_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Task Created',
            related_task=new_task
        )
        task_creation_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Task Created',
            related_task=new_task
        )

        self.assertEqual(task_creation_notifications_user1.count(), 1, "Task creation notification not created for user1")
        self.assertEqual(task_creation_notifications_user2.count(), 1, "Task creation notification not created for user2")

    def test_automatic_project_update_notification(self):
        """Test that a notification is created when a project is updated."""
        self.project.description = 'Updated Project Description'
        self.project.save()

        connection.commit()

        project_update_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Project Update',
            related_project=self.project
        )
        project_update_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Project Update',
            related_project=self.project
        )

        self.assertEqual(project_update_notifications_user1.count(), 1, "Project update notification not created for user1")
        self.assertEqual(project_update_notifications_user2.count(), 1, "Project update notification not created for user2")

    def test_send_task_reminders(self):
        """Test sending reminders for tasks with upcoming deadlines."""
        task_due_soon = Task.objects.create(
            owner=self.user1,
            project=self.project,
            title='Task Due Soon',
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(hours=12)  # Matches user1's reminder interval
        )

        call_command('send_reminders')
        connection.commit()

        reminder_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        reminder_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )

        self.assertEqual(reminder_notifications_user1.count(), 1, "Reminder notification not created for user1")
        self.assertEqual(reminder_notifications_user2.count(), 1, "Reminder notification not created for user2")

    def test_send_project_reminders(self):
        """Test sending reminders for projects ending soon."""
        # Set the project end date to exactly 12 hours from now
        self.project.end_date = (timezone.now() + timedelta(hours=12)).date()
        self.project.save()

        print(f"Project End Date: {self.project.end_date}")

        call_command('send_reminders')
        connection.commit()

        project_reminder_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Custom Reminder',
            related_project=self.project
        )
        print(f"Number of reminders for user1: {project_reminder_notifications_user1.count()}")

        project_reminder_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Custom Reminder',
            related_project=self.project
        )
        print(f"Number of reminders for user2: {project_reminder_notifications_user2.count()}")

        self.assertEqual(
            project_reminder_notifications_user1.count(),
            1,
            "Project reminder not created for user1"
        )
        self.assertEqual(
            project_reminder_notifications_user2.count(),
            1,
            "Project reminder not created for user2"
        )

    def test_mark_notification_as_read(self):
        """Test marking a notification as read."""
        notification = Notification.objects.create(
            recipient=self.user1,
            message='Test Notification',
            notification_type='Task Update',
            related_task=self.task,
            is_read=False
        )

        url = reverse('mark_notification_as_read', args=[notification.id])
        response = self.client.put(f"{url}?user_id={self.user1.id}", content_type='application/json')

        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_update_preferences(self):
        """Test updating notification preferences for a user."""
        url = reverse('update_preferences')
        data = {
            'receive_task_updates': False,
            'receive_project_updates': False,
            'receive_reminders': True,
            'custom_reminder_interval': 8
        }

        response = self.client.post(f"{url}?user_id={self.user1.id}", data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        user_pref = NotificationPreference.objects.get(user=self.user1)
        self.assertFalse(user_pref.receive_task_updates)
        self.assertFalse(user_pref.receive_project_updates)
        self.assertTrue(user_pref.receive_reminders)
        self.assertEqual(user_pref.custom_reminder_interval, 8)

    def test_get_preferences_user1(self):
        """Test retrieving notification preferences for user1."""
        response = self.client.get(reverse('get_preferences'), {'user_id': self.user1.id})

        self.assertEqual(response.status_code, 200)
        expected_response = {
            'receive_task_updates': True,
            'receive_project_updates': True,
            'receive_reminders': True,
            'custom_reminder_interval': 12
        }
        self.assertEqual(response.json(), expected_response)
