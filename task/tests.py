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


# class TaskAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create(
#             username='dohunWon',
#             email='wdh70743@gmail.com',
#             password=make_password('1234'),
#         )
#         self.user2 = User.objects.create(
#             username='user2',
#             email='user2@example.com',
#             password=make_password('1234'),
#         )
#         self.project = Project.objects.create(
#             owner=self.user,
#             projectname="TEST_PROJECT",
#             description="TEST",
#             start_date=datetime.now(),
#             end_date=datetime.now()
#         )
#         self.task = Task.objects.create(
#             owner=self.user,
#             project=self.project,
#             title='Test Task',
#             description='Test Description',
#             start_date='2024-09-28T00:00:00Z',
#             due_date='2024-10-28T00:00:00Z'
#         )
#         self.task_file = TaskFile.objects.create(
#             owner=self.user,
#             task=self.task,
#             file_uri='path/to/test_file.txt'
#         )
#
#     def test_create_task(self):
#         url = reverse('create_task')
#         data = {
#             'owner': self.user.id,
#             'project': self.project.id,
#             'title': 'New Task',
#             'description': 'New Description',
#             'start_date': '2024-09-29T00:00:00Z',
#             'due_date': '2024-10-29T00:00:00Z',
#             'task_file': [],
#             'user_ids': []
#         }
#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Task.objects.count(), 2)
#
#     def test_get_project_tasks(self):
#         url = reverse('project_tasks', kwargs={'project_id': self.project.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_get_user_tasks(self):
#         url = reverse('user_tasks', kwargs={'user_id': self.user.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_archive_task(self):
#         url = reverse('archive_task')
#         data = {'task_id': self.task.id}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertTrue(self.task.is_archived)
#
#     def test_get_user_archived_tasks(self):
#         self.task.is_archived = True
#         self.task.save()
#         url = reverse('user_archived_tasks', kwargs={'user_id': self.user.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_retrieve_task(self):
#         url = reverse('task_detail', kwargs={'pk': self.task.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Test Task')
#
#     def test_update_task(self):
#         url = reverse('task_detail', kwargs={'pk': self.task.id})
#         data = {'title': 'Updated Task'}
#         response = self.client.patch(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.task.refresh_from_db()
#         self.assertEqual(self.task.title, 'Updated Task')
#
#     def test_delete_task(self):
#         url = reverse('task_detail', kwargs={'pk': self.task.id})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Task.objects.count(), 0)
#
#     def test_assign_task_to_user(self):
#         url = reverse('assign-task')
#         data = {
#             'assigned_by': self.user.id,
#             'task_id': self.task.id,
#             'user_ids': [self.user2.id]
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(UserTask.objects.count(), 1)
#
#     def test_update_assigned_users(self):
#         UserTask.objects.create(task=self.task, assigned_to=self.user2, assigned_by=self.user)
#         url = reverse('update-assigned-users')
#         data = {
#             'assigned_by': self.user.id,
#             'task_id': self.task.id,
#             'user_ids': [self.user.id]  # Removing user2 and adding user
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(UserTask.objects.count(), 1)
#         self.assertEqual(UserTask.objects.first().assigned_to, self.user)
#
#     def test_get_assigned_task_list_from_project(self):
#         UserTask.objects.create(task=self.task, assigned_to=self.user, assigned_by=self.user)
#         url = reverse('get-assigned-tasks', kwargs={'project_id': self.project.id, 'user_id': self.user.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['assigned_tasks']), 1)
#
#     def test_create_file_and_get_file_list(self):
#         url = reverse('create-get-files', kwargs={'task_id': self.task.id})
#         file_content = b"file_content"
#         file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
#         data = {
#             'user_id': self.user.id,
#             'task_id': self.task.id,
#             'file_uri': file,
#         }
#         response = self.client.post(url, data, format='multipart')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # One existing file and one new file
class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create(
            username='testuser1',
            email='test1@example.com',
            password='test'
        )
        self.user2 = User.objects.create(
            username='testuser2',
            email='test2@example.com',
            password='test'
        )

        # Create test project
        self.project = Project.objects.create(
            owner=self.user,
            projectname="Test Project",
            description="Test Description",
            start_date=datetime.now(),
            end_date=datetime.now()
        )

        # Create test task
        self.task = Task.objects.create(
            owner=self.user,
            project=self.project,
            title='Test Task',
            description='Test Description',
            status=False,
            priority='Medium',
            start_date='2024-03-01T00:00:00Z',
            due_date='2024-03-31T00:00:00Z'
        )

    def test_create_task_basic(self):
        """Test creating a task with basic information"""
        url = reverse('create_task')
        data = {
            'owner': self.user.id,
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'High',
            'project': str(self.project.id),
            'start_date': '2024-03-15T00:00:00Z',
            'due_date': '2024-04-15T00:00:00Z',
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.priority, 'High')

    def test_create_task_with_files(self):
        """Test creating a task with file attachments"""
        url = reverse('create_task')
        file = SimpleUploadedFile(
            "test_file.txt",
            b"file_content",
            content_type="text/plain"
        )

        data = {
            'owner': self.user.id,
            'project': self.project.id,
            'title': 'Task with File',
            'description': 'Description',
            'start_date': '2024-03-15T00:00:00Z',
            'due_date': '2024-04-15T00:00:00Z',
            'uploaded_files': [file]
        }

        response = self.client.post(url, data, format='multipart')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_task = Task.objects.get(title='Task with File')
        self.assertEqual(new_task.files.count(), 1)

    def test_create_task_with_assignments(self):
        """Test creating a task with user assignments"""
        url = reverse('create_task')
        data = {
            'owner': self.user.id,
            'title': 'Task with Users',
            'description': 'Description',
            'project': self.project.id,
            'start_date': '2024-03-15T00:00:00Z',
            'due_date': '2024-04-15T00:00:00Z',
            'assigned_users': [self.user2.id]
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_task = Task.objects.get(title='Task with Users')
        self.assertEqual(new_task.user_tasks.count(), 1)
        self.assertEqual(new_task.user_tasks.first().assigned_to, self.user2)

    def test_update_task(self):
        """Test updating task information"""
        url = reverse('task_detail', kwargs={'pk': self.task.id})
        data = {
            'title': 'Updated Task',
            'priority': 'High'
        }
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.priority, 'High')

    def test_archive_task(self):
        """Test archiving and unarchiving a task"""
        url = reverse('archive_task')

        # Test archiving
        response = self.client.post(url, {'task_id': self.task.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertTrue(self.task.is_archived)

        # Verify task appears in archived list
        archived_url = reverse('user_archived_tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(archived_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_project_tasks(self):
        """Test retrieving all tasks for a project"""
        url = reverse('project_tasks', kwargs={'project_id': self.project.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_get_user_tasks(self):
        """Test retrieving all tasks for a user"""
        url = reverse('user_tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_task_assignment(self):
        """Test assigning and updating task assignments"""
        # Test initial assignment
        assign_url = reverse('assign-task')
        assign_data = {
            'assigned_by': self.user.id,
            'task_id': self.task.id,
            'user_ids': [self.user2.id]
        }

        response = self.client.post(assign_url, assign_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.user_tasks.count(), 1)

        # Test updating assignments
        update_url = reverse('update-assigned-users')
        update_data = {
            'assigned_by': self.user.id,
            'task_id': self.task.id,
            'user_ids': [self.user.id]  # Change assignment to first user
        }

        response = self.client.post(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.user_tasks.first().assigned_to, self.user)

    def test_delete_task(self):
        """Test deleting a task"""
        url = reverse('task_detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_get_assigned_tasks_from_project(self):
        """Test retrieving tasks assigned to a user within a project"""
        # Create assignment
        UserTask.objects.create(
            task=self.task,
            assigned_by=self.user,
            assigned_to=self.user2
        )

        url = reverse('get-assigned-tasks', kwargs={
            'project_id': self.project.id,
            'user_id': self.user2.id
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_tasks']), 1)

