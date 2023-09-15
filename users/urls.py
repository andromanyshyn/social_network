from django.urls import path

from users.views import CustomObtainAuthToken, UserAPIView

urlpatterns = [
    path("register/", UserAPIView.as_view(), name="registration"),
    path("auth/", CustomObtainAuthToken.as_view(), name="auth"),
]
