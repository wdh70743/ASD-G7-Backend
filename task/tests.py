from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from project.models import Project
from .models import Task, TaskFile, UserTask
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import SimpleUploadedFile


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='dohunWon',
            email='wdh70743@gmail.com',
            password=make_password('1234'),
        )
        self.user2 = User.objects.create(
            username='user2',
            email='user2@example.com',
            password=make_password('1234'),
        )
        self.project = Project.objects.create(
            owner=self.user,
            projectname="TEST_PROJECT",
            description="TEST",
            start_date=datetime.now(),
            end_date=datetime.now()
        )
        self.task = Task.objects.create(
            owner=self.user,
            project=self.project,
            title='Test Task',
            description='Test Description',
            start_date='2024-09-28T00:00:00Z',
            due_date='2024-10-28T00:00:00Z'
        )
        self.task_file = TaskFile.objects.create(
            owner=self.user,
            task=self.task,
            file_name='test_file.txt',
            file_uri='path/to/test_file.txt'
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

    def test_assign_task_to_user(self):
        url = reverse('assign-task')
        data = {
            'assigned_by': self.user.id,
            'task_id': self.task.id,
            'user_ids': [self.user2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserTask.objects.count(), 1)

    def test_update_assigned_users(self):
        UserTask.objects.create(task=self.task, assigned_to=self.user2, assigned_by=self.user)
        url = reverse('update-assigned-users')
        data = {
            'assigned_by': self.user.id,
            'task_id': self.task.id,
            'user_ids': [self.user.id]  # Removing user2 and adding user
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserTask.objects.count(), 1)
        self.assertEqual(UserTask.objects.first().assigned_to, self.user)

    def test_get_assigned_task_list_from_project(self):
        UserTask.objects.create(task=self.task, assigned_to=self.user, assigned_by=self.user)
        url = reverse('get-assigned-tasks', kwargs={'project_id': self.project.id, 'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_tasks']), 1)

    def test_create_file_and_get_file_list(self):
        url = reverse('create-get-files', kwargs={'task_id': self.task.id})
        file_content = b"file_content"
        file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
        data = {
            'user_id': self.user.id,
            'task_id': self.task.id,
            'file_name': 'new_test_file.txt',
            'file_uri': file,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # One existing file and one new file

    def test_delete_and_update_file(self):
        url = reverse('files-details', kwargs={'id': self.task_file.id})

        # Test update
        data = {'file_name': 'updated_test_file.txt'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_file.refresh_from_db()
        self.assertEqual(self.task_file.file_name, 'updated_test_file.txt')

        # Test delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskFile.objects.count(), 0)
