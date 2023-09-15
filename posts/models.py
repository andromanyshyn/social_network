from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=32)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Post {self.title} by {self.user.username} at {self.created_at}"
