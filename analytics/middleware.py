import logging

from django.utils import timezone

logger = logging.getLogger(__name__)


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        if user.is_authenticated:
            logger.info(f"User {request.user.username} made a request at {timezone.now()}")
        return response
