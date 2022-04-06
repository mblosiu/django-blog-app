from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from .models import CustomUser


class UsersTestCase(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create(username="testuser", email="testuser@email.com")
        user.set_password("Password123")
        user.save()

    def test_registration(self):
        response = self.client.post('/api/users/',
                                    {'username': 'testuser2', 'email': 'testuser2@email.com', 'password': 'Password123',
                                     'password2': 'Password123'}, format='json')
        print(response)
        self.assertEqual(response.status_code, 201)

    def test_token(self):
        response = self.client.post('/api/users/token/', {'username': 'testuser', 'password': 'Password123'},
                                    format='json')
        self.assertIsNotNone(response.data.get('access'))
        self.assertIsNotNone(response.data.get('refresh'))
        self.assertEqual(response.status_code, 200)

    def test_refresh(self):
        response = self.client.post('/api/users/token/', {'username': 'testuser', 'password': 'Password123'},
                                    format='json')

        response2 = self.client.post('/api/users/token/refresh/', {'refresh': response.data.get('refresh')},
                                     format='json')

        self.assertEqual(response2.status_code, 200)

    def test_users_list(self):
        response = self.client.get('/api/users/', {}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_users_detail(self):
        user = CustomUser.objects.all().first()

        response = self.client.get('/api/users/' + str(user.id) + '/', {}, format='json')
        self.assertEqual(response.status_code, 200)
