from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import ChatbotMessage, GeneratedQuiz, ProgramRecommendation, PerformanceTracking
from .serializers import (
    ChatbotMessageSerializer,
    GeneratedQuizSerializer,
    ProgramRecommendationSerializer,
    PerformanceTrackingSerializer,
)

def index(request):
    return HttpResponse("Welcome to Ai-endpoint")
def chatbot_messages_view(request):
    return HttpResponse("chatbot-messages-endpoint")

def generated_quizzes_view(request):
    return HttpResponse("generated-quizzes-endpoint")

def program_recommendations_view(request):
    return HttpResponse("program-recommendations-endpoint")

def performance_tracking_view(request):
    return HttpResponse("performance-tracking-endpoint")




# 💬 Chatbot messages
class ChatbotMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🧠 Generated quizzes
class GeneratedQuizListCreateView(generics.ListCreateAPIView):
    queryset = GeneratedQuiz.objects.all()
    serializer_class = GeneratedQuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📘 Program recommendations
class ProgramRecommendationListCreateView(generics.ListCreateAPIView):
    queryset = ProgramRecommendation.objects.all()
    serializer_class = ProgramRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 📊 Performance tracking
class PerformanceTrackingListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceTracking.objects.all()
    serializer_class = PerformanceTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
