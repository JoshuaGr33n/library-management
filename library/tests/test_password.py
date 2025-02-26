from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="oldpassword")
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        url = reverse('change-password')
        data = {
            "old_password": "oldpassword",
            "new_password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_change_password_invalid_old_password(self):
        url = reverse('change-password')
        data = {
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_change_password_weak_new_password(self):
        url = reverse('change-password')
        data = {
            "old_password": "oldpassword",
            "new_password": "weak"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)