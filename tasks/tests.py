from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class TaskTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='123456')

    def test_register(self):
        response = self.client.post('/api/register/', {
            'username': 'user1',
            'password': '123456'
        })
        self.assertEqual(response.status_code, 201)