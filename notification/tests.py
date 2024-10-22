# notification/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from notification.models import Notification, NotificationPreference
from task.models import Task
from users.models import User
from project.models import Project
from datetime import timedelta

class NotificationTests(TestCase):

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
            end_date=timezone.now() + timedelta(days=10)
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

        # Set up client
        self.client = Client()

    def test_notification_list(self):
        """Test retrieving a list of notifications for a user (U901)"""
        # Create test notifications
        Notification.objects.create(
            recipient=self.user1,
            message='Task Updated',
            notification_type='Task Update',
            related_task=self.task
        )
        Notification.objects.create(
            recipient=self.user1,
            message='Project Updated',
            notification_type='Project Update',
            related_project=self.project
        )

        # Send GET request to list notifications
        response = self.client.get(reverse('notification_list'), {'user_id': self.user1.id})

        # Check if response status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response content to JSON
        response_data = response.json()

        # Debug print to verify response data structure
        print("Response JSON:", response_data)

        # Verify response length is 2
        self.assertEqual(len(response_data), 2)

        # Check that the response contains the expected messages
        messages = {notification['message'] for notification in response_data}
        self.assertIn('Task Updated', messages)
        self.assertIn('Project Updated', messages)

    def test_mark_notification_as_read(self):
        """Test marking a notification as read (U904)"""
        # Create a test notification
        notification = Notification.objects.create(
            recipient=self.user1,
            message='Test Notification',
            notification_type='Task Update',
            related_task=self.task,
            is_read=False
        )

        # Send PUT request to mark notification as read
        url = reverse('mark_notification_as_read', args=[notification.id])
        response = self.client.put(f"{url}?user_id={self.user1.id}", content_type='application/json')

        # Check if response is 200 and notification is marked as read
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_update_preferences(self):
        """Test updating notification preferences for a user (U903)"""
        # Prepare request data
        url = reverse('update_preferences')
        data = {
            'receive_task_updates': False,
            'receive_project_updates': False,
            'receive_reminders': True,
            'custom_reminder_interval': 8
        }

        # Send POST request to update notification preferences
        response = self.client.post(f"{url}?user_id={self.user1.id}", data, content_type='application/json')

        # Check if response is 200 and preferences are updated
        self.assertEqual(response.status_code, 200)
        user_pref = NotificationPreference.objects.get(user=self.user1)
        self.assertFalse(user_pref.receive_task_updates)
        self.assertFalse(user_pref.receive_project_updates)
        self.assertTrue(user_pref.receive_reminders)
        self.assertEqual(user_pref.custom_reminder_interval, 8)

    def test_send_reminders(self):
        """Test sending reminders for upcoming task deadlines (U902, U905)"""
        # Create a task with a due date within the custom reminder interval
        task_due_soon = Task.objects.create(
            owner=self.user1,
            project=self.project,
            title='Task Due Soon',
            description='A task due soon',
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(hours=12)  # Matches user1's reminder interval
        )

        # Run the management command to send reminders
        from django.core.management import call_command
        call_command('send_reminders')

        # Check if a reminder notification was created for user1
        reminder_notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(reminder_notifications.count(), 1)

        # Ensure no reminder for user2 (custom interval of 6 hours)
        reminder_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(reminder_notifications_user2.count(), 0)

    def test_task_update_notification(self):
        """Test task update notifications based on preferences (U901)"""
        # Update task title
        self.task.title = 'Updated Task Title'
        self.task.save()

        # Directly create the notification for user1
        if self.user1.notification_preference.receive_task_updates:
            Notification.objects.create(
                recipient=self.user1,
                message=f'Task "{self.task.title}" has been updated.',
                notification_type = 'Task Update',
                related_task = self.task
            )

        # Check if a task update notification was created for user1
        task_update_notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Task Update',
            related_task=self.task
        )
        self.assertEqual(task_update_notifications.count(), 1)

        # Ensure no task update notification for user2 (does not receive task updates)
        task_update_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Task Update',
            related_task=self.task
        )
        self.assertEqual(task_update_notifications_user2.count(), 0)

    def test_project_update_notification(self):
        """Test project update notifications based on preferences (U904)"""
        # Update project description
        self.project.description = 'Updated Project Description'
        self.project.save()

        # Directly create the notification for project update
        for user in self.project.users.all():
            if user.notification_preference.receive_project_updates:
                Notification.objects.create(
                    recipient=user,
                    message=f'Project "{self.project.projectname}" has been updated.',
                    notification_type='Project Update',
                    related_project=self.project
                )

        # Check if a project update notification was created for both users
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
        self.assertEqual(project_update_notifications_user1.count(), 1)
        self.assertEqual(project_update_notifications_user2.count(), 1)