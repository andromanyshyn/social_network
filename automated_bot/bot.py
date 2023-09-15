import csv
from random import choice, choices, randint, randrange
from string import ascii_letters, ascii_lowercase, digits

import requests
from rest_framework import status

API_URL = "http://localhost:8000/api/v1/"


# Create a Config class to read configuration data from a CSV file
class Config:
    def __init__(self, name):
        self.filename = name

    def read_config(self):
        config_data = []
        with open(self.filename, "r") as config:
            csvreader = csv.DictReader(config)
            for row in csvreader:
                config_data.append(row)
        return config_data


# Create a Bot class to handle user sign-up, authorization, post creation, and liking
class Bot:
    def __init__(self, url, config):
        self.url = url
        self.config = config
        self.number_of_users = None
        self.max_posts_per_user = None
        self.max_likes_per_user = None

    # Retrieve configuration data from the CSV file
    def get_config_data(self):
        for row in self.config:
            self.number_of_users = int(row["number_of_users"])
            self.max_posts_per_user = int(row["max_posts_per_user"])
            self.max_likes_per_user = int(row["max_likes_per_user"])

    # Handle user sign-up
    def run(self):
        self.get_config_data()
        for _ in range(self.number_of_users):
            # Generate a random username and password
            username = "".join(choices(ascii_lowercase, k=8)) + str(randint(100, 1000))
            password = "".join(choices(ascii_letters + digits, k=10))

            data = {"username": username, "password": password}

            # Send a POST request to register the user
            response = requests.post(self.url + "users/register/", data=data)
            if response.status_code == status.HTTP_201_CREATED:
                print(f"[INFO] - User {data['username']} signed up")
                user_data = response.json()
                user_data["password"] = data["password"]
                user = user_data["id"]
                token = self.authorization(user_data)

                # Create posts and like them
                posts = self.create_post(user, token)
                self.like_post(user, choice(posts), token)
            else:
                print(f"Error while creating the user: {response.status_code}")
                return None

    # Handle user authorization
    def authorization(self, data):
        response = requests.post(self.url + "users/auth/", data=data)
        if response.status_code == status.HTTP_200_OK:
            print(f"[INFO] - User {data['username']} logged in")
            token = response.json().get("token")
            return token
        else:
            print(f"Error while authorization: {response.status_code}")
            return None

    # Handle post creation
    def create_post(self, user_id, token):
        posts = []
        headers = {"Authorization": f"Bearer {token}"}

        num_posts = randrange(1, self.max_posts_per_user + 1)

        for _ in range(num_posts):
            # Generate random post title and content
            title = "".join(choices(ascii_letters, k=10))
            content = "".join(choices(ascii_letters + digits, k=30))

            data = {"user_id": user_id, "title": title, "content": content}

            # Send a POST request to create a post
            response = requests.post(self.url + "posts/", data=data, headers=headers)
            if response.status_code == status.HTTP_201_CREATED:
                print(f"[INFO] - Post {data['title']} has been created by user_id: {user_id}")
                post_id = response.json()["id"]
                posts.append(post_id)
            else:
                print(f"Error while creating the post: {response.status_code}")
                return None
        return posts

    # Handle liking a post
    def like_post(self, user_id, post_id, token):
        headers = {"Authorization": f"Bearer {token}"}
        actions = ["Like", "Dislike"]

        num_likes = randrange(1, self.max_likes_per_user + 1)
        for _ in range(num_likes):
            data = {"user_id": user_id, "post_id": post_id, "action": choice(actions)}

            # Send a POST request to like or dislike a post
            response = requests.post(self.url + "posts/activity/", data=data, headers=headers)
            if response.status_code == status.HTTP_200_OK:
                print(f"[INFO] - Post ID : {data['post_id']} | Action {data['action']} | By user_id {data['user_id']}")
            else:
                print(f"Error while liking the post: {response.status_code}")
                return None


if __name__ == "__main__":
    # Create an instance of the Config class to read the configuration data
    conf = Config("config.csv")
    config = conf.read_config()

    # Create an instance of the Bot class and perform sign-up and other actions
    bot = Bot(API_URL, config)
    bot.run()
