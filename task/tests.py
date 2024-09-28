from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from project.models import Project
from .models import Task
from django.contrib.auth.hashers import make_password


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='dohunWon',
            email='wdh70743@gmail.com',
            password=make_password('1234'),
        )
        self.project = Project.objects.create(projectname="TEST_PROJECT", description="TEST", start_date=datetime.now(),
                                              end_date=datetime.now())
        self.task = Task.objects.create(
            owner=self.user,
            project=self.project,
            title='Test Task',
            description='Test Description',
            start_date='2024-09-28T00:00:00Z',
            due_date='2024-10-28T00:00:00Z'
        )

    def test_create_task(self):
        url = reverse('create_task')
        data = {
            'owner': self.user.id,
            'project': self.project.id,
            'title': 'New Task',
            'description': 'New Description',
            'start_date': '2024-09-29T00:00:00Z',
            'due_date': '2024-10-29T00:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_project_tasks(self):
        url = reverse('project_tasks', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_tasks(self):
        url = reverse('user_tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_archive_task(self):
        url = reverse('archive_task')
        data = {'task_id': self.task.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

    def test_get_user_archived_tasks(self):
        self.task.is_archived = True
        self.task.save()
        url = reverse('user_archived_tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_task(self):
        url = reverse('task_detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        url = reverse('task_detail', kwargs={'pk': self.task.id})
        data = {'title': 'Updated Task'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        url = reverse('task_detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
