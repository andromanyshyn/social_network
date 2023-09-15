from random import choices, randint
from string import ascii_letters, ascii_lowercase, digits

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class RegisterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model()

    @staticmethod
    def generate_true_data(count):
        users = []
        for _ in range(count):
            username = "".join(choices(ascii_lowercase, k=8)) + str(randint(100, 1000))
            password = "".join(choices(ascii_letters + digits, k=10))
            users.append(
                {
                    "password": password,
                    "username": username,
                }
            )
        return users

    def test_register(self):
        users = self.generate_true_data(3)

        # create check
        for user in users:
            response = self.client.post(reverse("registration"), user, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["username"], user["username"])
            self.assertTrue(self.user.objects.filter(username=user["username"]).exists())
            users[users.index(user)]["id"] = response.data["id"]

        # authenticate
        for user in users:
            response = self.client.post(
                reverse("auth"),
                {"password": user["password"], "username": user["username"]},
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["token"], Token.objects.get(user_id=user["id"]).key)
            users[users.index(user)]["token"] = response.data["token"]
