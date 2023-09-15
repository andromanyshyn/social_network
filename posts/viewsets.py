from rest_framework import status, viewsets
from rest_framework.response import Response

from analytics.tasks import track_post_activity
from posts.models import Post
from posts.permissions import CanInteractWithPostAPI
from posts.serializers import PostSerializer


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (CanInteractWithPostAPI,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def activity(self, request):
        track_post_activity.delay(
            user_id=request.data["user_id"], post_id=request.data["post_id"], action=request.data["action"]
        )
        return Response(
            {"status": status.HTTP_201_CREATED, "message": "the action for the post was completed successfully"}
        )
