from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from reservations.admin import admin_site

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("admin/", admin_site.urls),
    path("", include("reservations.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
