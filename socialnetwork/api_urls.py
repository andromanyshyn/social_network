from django.urls import include, path

urlpatterns = [
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("analytics/", include("analytics.urls")),
]
