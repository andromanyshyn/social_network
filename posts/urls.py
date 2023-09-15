from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.viewsets import PostAPIViewSet

router = DefaultRouter()
router.register("", PostAPIViewSet, basename="posts")

urlpatterns = [
    path("activity/", PostAPIViewSet.as_view({"post": "activity"}), name="post-activity"),
    path("", include(router.urls)),
]
