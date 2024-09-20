from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import User


# Create your tests here.


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='dohunWon',
            email='wdh70743@gmail.com',
            password=make_password('1234'),
        )

    def test_create_user(self):
        url = reverse('create_user')
        data = {
            'email': 'newuser@gmail.com',
            'username': 'abcd',
            'password': 'newpassword1234'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertNotEqual(response.data['password'], data['password'])

    def test_create_user_missing_password(self):
        url = reverse('create_user')
        data = {
            'email': 'newuser@gmail.com',
            'username': 'abcd',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Password is required')

    def test_login_user(self):
        url = reverse('login_user')

        data = {
            'email': 'wdh70743@gmail.com',
            'password': '1234'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_login_invalid_credentials(self):
        url = reverse('login_user')
        data = {
            'email': 'wdh70743@gmail.com',
            'password': '123456'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_get_user_details(self):
        url = reverse('retrieve_update_destroy_user', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_partial_update_user_details(self):
        url = reverse('retrieve_update_destroy_user', kwargs={'pk': self.user.pk})
        data = {
            'email': 'updated@example.com',
            'username': 'updated'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])

    def test_update_user_details(self):
        url = reverse('retrieve_update_destroy_user', kwargs={'pk': self.user.pk})
        data = {
            'email': 'updated@example.com',
            'username': 'updated',
            'password': 'updated1234'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])

    def test_delete_user(self):
        url = reverse('retrieve_update_destroy_user', kwargs={'pk': self.user.pk})
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
