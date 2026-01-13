from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CitizenLab Chatbot API",
        default_version="v1",
        description="API officielle du chatbot institutionnel CitizenLab Sénégal",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.chatbot.urls")),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]
