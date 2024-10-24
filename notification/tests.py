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
from django.db import connection, transaction


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
            receive_reminders=False,
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

        self.client = Client()

    def test_notification_list(self):
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

        response = self.client.get(reverse('notification_list'), {'user_id': self.user1.id})

        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        self.assertEqual(len(response_data), 2)

        messages = {notification['message'] for notification in response_data}
        self.assertIn('Task Updated', messages)
        self.assertIn('Project Updated', messages)

    def test_automatic_task_update_notification(self):

        self.task.title = 'Updated Task Title'
        self.task.save()

        task_update_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Task Update',
            related_task=self.task
        )

        self.assertEqual(
            task_update_notifications_user1.count(),
            1,
            "Task update notification not created for user1"
        )

    def test_automatic_project_update_notification(self):

        self.project.description = 'Updated Project Description'
        self.project.save()

        # Manually commit the transaction to ensure the signal triggers
        connection.commit()

        # Check if a project update notification was automatically created for user1 and user2
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

        self.assertEqual(
            project_update_notifications_user1.count(),
            1,
            "Project update notification not created for user1"
        )
        self.assertEqual(
            project_update_notifications_user2.count(),
            1,
            "Project update notification not created for user2"
        )

    def test_automatic_task_due_reminder(self):
        """Test that a reminder notification is automatically created for tasks with due dates approaching."""
        # Create a task with a due date within the custom reminder interval
        task_due_soon = Task.objects.create(
            owner=self.user1,
            project=self.project,
            title='Task Due Soon',
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(hours=12)  # Matches user1's reminder interval
        )

        # Run the management command to send reminders
        call_command('send_reminders')

        # Manually commit the transaction to ensure the signal triggers
        connection.commit()

        # Check if a reminder notification was automatically created for user1
        reminder_notifications_user1 = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(
            reminder_notifications_user1.count(),
            1,
            "Reminder notification not created for user1"
        )

        # Ensure no reminder for user2
        reminder_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(
            reminder_notifications_user2.count(),
            0,
            "Unexpected reminder notification for user2"
        )

    def test_mark_notification_as_read(self):
        """Test marking a notification as read."""
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
        """Test updating notification preferences for a user."""
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
        """Test sending reminders for upcoming task deadlines."""
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
        call_command('send_reminders')

        # Manually commit the transaction to ensure the signal triggers
        connection.commit()

        # Check if a reminder notification was created for user1
        reminder_notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(
            reminder_notifications.count(),
            1,
            "Reminder notification not created for user1"
        )

        # Ensure no reminder for user2
        reminder_notifications_user2 = Notification.objects.filter(
            recipient=self.user2,
            notification_type='Custom Reminder',
            related_task=task_due_soon
        )
        self.assertEqual(
            reminder_notifications_user2.count(),
            0,
            "Unexpected reminder notification for user2"
        )

    def test_get_preferences_user1(self):
        """Test retrieving notification preferences for user1."""
        response = self.client.get(reverse('get_preferences'), {'user_id': self.user1.id})

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        print("Response data:", response.json())
        # Check if the response contains correct preferences for user1
        expected_response = {
            'receive_task_updates': True,
            'receive_project_updates': True,
            'receive_reminders': True,
            'custom_reminder_interval': 12
        }
        self.assertEqual(response.json(), expected_response)

    def test_get_preferences_user_not_found(self):
        """Test retrieving preferences for a non-existent user."""
        response = self.client.get(reverse('get_preferences'), {'user_id': 999})  # Non-existent user ID

        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Check if the response contains the correct error message
        expected_response = {'error': 'User not found'}
        self.assertEqual(response.json(), expected_response)

    def test_get_preferences_without_user_id(self):
        """Test retrieving preferences without providing user_id."""
        response = self.client.get(reverse('get_preferences'))

        # Check if the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Check if the response contains the correct error message
        expected_response = {'error': 'User ID is required'}
        self.assertEqual(response.json(), expected_response)

