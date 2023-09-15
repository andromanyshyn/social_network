from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from analytics.tasks import track_user_sign_in
from users.serializers import UserSerializer

User = get_user_model()


class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data["username"])
            track_user_sign_in.delay(user.id)
        return response
