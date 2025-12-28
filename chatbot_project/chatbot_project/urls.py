from django.http import HttpResponse
from django.urls import path
from chatbot_api.views import ChatbotView

def home(request):
    return HttpResponse("Chatbot backend is running. Use /chat/ to send queries.")

urlpatterns = [
    path("", home),
    path("chat/", ChatbotView.as_view(), name="chat"),
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
