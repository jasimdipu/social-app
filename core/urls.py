"""social URL Configuration"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        "api/v1/accounts/", include(("users.urls", "users"))
    ),
    re_path(
        "api/v1/friends/", include(("friends.urls", "friends"))
    ),
    path("api/v1/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path(
        "api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(), name="swagger-ui"
    ),
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(), name="redoc"),
]
