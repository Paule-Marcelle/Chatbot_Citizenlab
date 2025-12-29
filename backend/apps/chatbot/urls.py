from django.urls import path
from .api.views import ChatbotAPIView

urlpatterns = [
    path("chat/", ChatbotAPIView.as_view(), name="chatbot-api"),
]
