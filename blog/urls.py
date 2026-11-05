from django.urls import include, path

urlpatterns = [
    path("api/", include("accounts.urls")),
    path("api/", include("posts.urls")),
    path("api/", include("comments.urls")),
]
