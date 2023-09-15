import re

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.filters import PostAnalyticFilter
from analytics.models import PostActivity, UserActivity
from analytics.permissions import CanInteractWithPostAnalyticAPI
from analytics.serializers import PostActivitySerializer

User = get_user_model()


class PostAnalyticAPIView(generics.ListAPIView):
    queryset = PostActivity.objects.all()
    serializer_class = PostActivitySerializer
    permission_classes = (CanInteractWithPostAnalyticAPI,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostAnalyticFilter

    # Filter and annotate the queryset to calculate likes count by date
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = (
            queryset.annotate(date_action=TruncDate("occurred_at"))
            .values("date_action")
            .annotate(likes_count=Count("id"))
        )
        return Response({"status": status.HTTP_200_OK, "data": queryset})


class UserAnalyticAPIView(APIView):
    @staticmethod
    def post(request):
        user = get_object_or_404(User, id=request.data["user_id"])
        action = UserActivity.Actions.SIGN_IN.value

        # Find the last user login activity record
        last_login = UserActivity.objects.filter(user=user, action=action).last()
        try:
            with open("user_requests.log", encoding="utf-8") as file:
                users_log = [line for line in file.readlines() if user.username in line]
                last_log = users_log[-1]

                datetime_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

                # Search for the datetime pattern in the last log entry
                match = re.search(datetime_pattern, last_log)

        except FileNotFoundError:
            print("File 'user_requests.log' not found.")

        message = f"User {user.username} didn`t perform this action"

        # Prepare the response data with user's last login and last request
        data = {
            "users_last_login": last_login.occurred_at if last_login else message,
            "users_last_request": match.group() if match else message,
        }
        return Response({"status": status.HTTP_200_OK, "data": data})
