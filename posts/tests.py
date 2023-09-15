from random import choices, randint
from string import ascii_letters, ascii_lowercase, digits

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post


class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model()
        self.posts = Post.objects.all()

    @staticmethod
    def generate_users_data(count):
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

    def generate_posts_data(self):
        posts = []
        for user in self.user.objects.all():
            title = "".join(choices(ascii_letters, k=10))
            content = "".join(choices(ascii_letters + digits, k=30))
            posts.append(
                {
                    "user": user.id,
                    "title": title,
                    "content": content,
                }
            )
            self.client.force_authenticate(user=user)
        return posts

    def test_post_creation(self):
        users = self.generate_users_data(3)

        # create user
        for user in users:
            response = self.client.post(reverse("registration"), user, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["username"], user["username"])
            self.assertTrue(self.user.objects.filter(username=user["username"]).exists())

        # create post
        posts = self.generate_posts_data()

        for post in posts:
            response = self.client.post(reverse("posts-list"), post, format="json")

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["title"], post["title"])
            self.assertEqual(response.data["content"], post["content"])
            self.assertTrue(self.posts.filter(title=post["title"]).exists())
