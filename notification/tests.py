from django.test import TestCase, Client
from django.urls import reverse
from notification.models import Notification, NotificationPreference
from users.models import User

class NotificationTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client = Client()

        # Create test notifications for the user
        Notification.objects.create(
            recipient=self.user,
            message='Test notification 1',
            notification_type='Task Update',
            is_read=False
        )
        Notification.objects.create(
            recipient=self.user,
            message='Test notification 2',
            notification_type='Project Update',
            is_read=True
        )

        # Create test notification preferences for the user
        NotificationPreference.objects.create(
            user=self.user,
            receive_task_updates=True,
            receive_project_updates=True,
            receive_reminders=True
        )

    def test_notification_list(self):
        # Send GET request to list notifications with user_id
        response = self.client.get(reverse('notification_list'), {'user_id': self.user.id})

        # Check if response is 200 and contains notifications
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_mark_notification_as_read(self):
        # Mark the first notification as read
        notification = Notification.objects.filter(recipient=self.user, is_read=False).first()

        # Send PUT request to mark notification as read with user_id as query parameter
        url = reverse('mark_notification_as_read', args=[notification.id])
        response = self.client.put(f"{url}?user_id={self.user.id}", content_type='application/json')

        # Check if response is 200 and notification is marked as read
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_update_preferences(self):
        # Prepare request data and URL
        url = reverse('update_preferences')
        data = {
            'receive_task_updates': False,
            'receive_project_updates': False,
            'receive_reminders': False
        }

        # Send POST request to update notification preferences with user_id as query parameter
        response = self.client.post(f"{url}?user_id={self.user.id}", data, content_type='application/json')

        # Check if response is 200 and preferences are updated
        self.assertEqual(response.status_code, 200)
        pref = NotificationPreference.objects.get(user=self.user)
        self.assertFalse(pref.receive_task_updates)
        self.assertFalse(pref.receive_project_updates)
        self.assertFalse(pref.receive_reminders)
