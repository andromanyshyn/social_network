from django.urls import path

from analytics.views import PostAnalyticAPIView, UserAnalyticAPIView

urlpatterns = [
    path("post/", PostAnalyticAPIView.as_view(), name="likes_analytics"),
    path("user/", UserAnalyticAPIView.as_view(), name="user_activity_analytics"),
]
