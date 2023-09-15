from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class PostActivity(models.Model):
    class Actions(models.TextChoices):
        LIKE = "LIKE", "Like"
        DISLIKE = "DISLIKE", "Dislike"

    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="posts_analytics")
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="analytics")
    action = models.CharField(max_length=7, choices=Actions.choices)
    occurred_at = models.DateField()

    def __str__(self):
        return f"User {self.user.username} - Action {self.action}"


class UserActivity(models.Model):
    class Actions(models.TextChoices):
        SIGN_IN = "SIGN IN", "Sign In"

    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="actions")
    action = models.CharField(max_length=7, choices=Actions.choices, null=True, blank=True)
    occurred_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - Action {self.action}"
