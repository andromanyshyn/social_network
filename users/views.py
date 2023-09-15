from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from analytics.tasks import track_user_sign_in
from users.serializers import UserSerializer

User = get_user_model()


# Define a view for creating User objects using generics
class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Define a custom ObtainAuthToken view
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data["username"])

            # Use Celery to asynchronously track the user sign-in
            track_user_sign_in.delay(user.id)
        return response
