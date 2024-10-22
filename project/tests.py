from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from notification.models import Notification, NotificationPreference

class NotificationAPITests(APITestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')

        # Create a client instance
        self.client = APIClient()

        # Create notifications for the user
        self.notification1 = Notification.objects.create(
            recipient=self.user,
            message='Test notification 1',
            notification_type='Task Update',
            is_read=False
        )
        self.notification2 = Notification.objects.create(
            recipient=self.user,
            message='Test notification 2',
            notification_type='Project Update',
            is_read=True
        )

        # Create notification preferences for the user
        self.preferences = NotificationPreference.objects.create(
            user=self.user,
            receive_task_updates=True,
            receive_project_updates=True,
            receive_reminders=True
        )

    def test_notification_list(self):
        # Send GET request to list notifications
        url = reverse('notification_list')
        response = self.client.get(f"{url}?user_id={self.user.id}", format='json')

        # Check if response is 200 and contains notifications
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_mark_notification_as_read(self):
        # Mark the first notification as read
        url = reverse('mark_notification_as_read', args=[self.notification1.id])
        response = self.client.put(f"{url}?user_id={self.user.id}", format='json')

        # Check if response is 200 and notification is marked as read
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)

    def test_update_preferences(self):
        # Prepare data for updating preferences
        url = reverse('update_preferences')
        data = {
            'receive_task_updates': False,
            'receive_project_updates': False,
            'receive_reminders': False
        }

        # Send POST request to update preferences
        response = self.client.post(f"{url}?user_id={self.user.id}", data, format='json')

        # Check if response is 200 and preferences are updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.preferences.refresh_from_db()
        self.assertFalse(self.preferences.receive_task_updates)
        self.assertFalse(self.preferences.receive_project_updates)
        self.assertFalse(self.preferences.receive_reminders)
