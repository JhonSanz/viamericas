from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from reservations.admin import admin_site
from reservations.views.health import health_check

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", include("reservations.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("health", health_check),
]
