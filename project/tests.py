from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from .models import Project

class ProjectAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='password1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', password='password2', email='user2@example.com')

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
        self.project.users.add(self.user1, self.user2)

        self.client = APIClient()

    def test_create_project(self):
        url = reverse('project-create')
        data = {
            "owner": self.user1.id,
            "projectname": "New Project",
            "description": "Testing project creation.",
            "start_date": "2024-10-01",
            "end_date": "2024-12-31",
            "priority": "Medium",
            "status": False,
            "user_ids": [self.user1.id, self.user2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['projectname'], data['projectname'])

    def test_list_projects(self):
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
