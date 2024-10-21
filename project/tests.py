from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from notification.models import Notification, NotificationPreference

class NotificationAPITests(APITestCase):

    def setUp(self):
<<<<<<< HEAD
        # Create users
        self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')
=======
        self.user1 = User.objects.create(username='user1', password='password1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', password='password2', email='user2@example.com')
        self.user3 = User.objects.create(username='user3', password='password3', email='user3@example.com')

        # Create a sample project
        self.project = Project.objects.create(
            owner=self.user1,
            projectname="Test Project",
            description="A test project.",
            start_date="2024-10-01",
            end_date="2024-12-31",
            priority="Medium",
            status=False
        )
        self.project.users.add(self.user2)
>>>>>>> 4390c64973c8e0b22f7e27ee8322a87ca9a1b232

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
<<<<<<< HEAD
        self.preferences.refresh_from_db()
        self.assertFalse(self.preferences.receive_task_updates)
        self.assertFalse(self.preferences.receive_project_updates)
        self.assertFalse(self.preferences.receive_reminders)
=======
        self.assertEqual(len(response.data), 1)  # Should return 1 project created in setUp

    def test_retrieve_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['projectname'], self.project.projectname)

    def test_update_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project.id})
        data = {
            "projectname": "Updated Project",
            "description": "Updated description",
            "start_date": "2024-10-01",
            "end_date": "2024-12-31",
            "priority": "High",
            "status": True,
            "user_ids": [self.user1.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.projectname, "Updated Project")
        self.assertEqual(self.project.priority, "High")

    def test_delete_project(self):
        url = reverse('project-detail', kwargs={'pk': self.project.id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)  # Project should be deleted

    def test_list_user_projects(self):
        url = reverse('user-projects', kwargs={'user_id': self.user1.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # User1 is associated with 1 project

    def test_search_user_in_project(self):
        url = reverse('project-user-search', kwargs={'project_id': self.project.id})

        response = self.client.get(f"{url}?email=user1", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'user1@example.com')

        response = self.client.get(f"{url}?email=user2", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'user2@example.com')

        response = self.client.get(f"{url}?email=user3", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(f"{url}?email=user", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both user1 and user2

        response = self.client.get(f"{url}?email=USER1", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'user1@example.com')

        url = reverse('project-user-search', kwargs={'project_id': 9999})
        response = self.client.get(f"{url}?email=user1", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('project-user-search', kwargs={'project_id': self.project.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
>>>>>>> 4390c64973c8e0b22f7e27ee8322a87ca9a1b232
