from celery import shared_task
from django.utils import timezone

from analytics.models import PostActivity, UserActivity


@shared_task
def track_post_activity(user_id, post_id, action):
    if action == "Like":
        action = PostActivity.Actions.LIKE.value
    else:
        action = PostActivity.Actions.DISLIKE.value
    PostActivity.objects.create(user_id=user_id, post_id=post_id, action=action, occurred_at=timezone.now())


@shared_task
def track_user_sign_in(user_id):
    action = UserActivity.Actions.SIGN_IN.value
    UserActivity.objects.create(user_id=user_id, action=action, occurred_at=timezone.now())
