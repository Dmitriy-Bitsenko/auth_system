from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "middle_name": "Middle",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

    def test_register(self):
        url = reverse("register")
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_login(self):
        self.test_register()
        url = reverse("login")
        data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_profile(self):
        self.test_login()
        token = self.client.post(reverse("login"), {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json").data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_logout(self):
        self.test_login()
        token = self.client.post(reverse("login"), {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json").data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
