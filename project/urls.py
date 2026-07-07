
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from banda.api import api as banda_api

## project/urls.py

urlpatterns = [
    path("admin/", admin.site.urls),
    path("escola/", include("escola.urls")), 
    path("", include("portofolio.urls")),
    path("api/", banda_api.urls),
    path("accounts/", include("accounts.urls")),
    path("artigos/", include("artigos.urls")),
]
