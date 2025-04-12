from django.urls import path
from . import views
from .views import (
    ChatbotMessageListCreateView,
    GeneratedQuizListCreateView,
    ProgramRecommendationListCreateView,
    PerformanceTrackingListCreateView,
)

urlpatterns = [
    path('', views.index, name='ai-home'),
    path('chatbot/', ChatbotMessageListCreateView.as_view(), name='chatbot-messages'),                   # GET + POST
    path('generated-quizzes/', GeneratedQuizListCreateView.as_view(), name='generated-quizzes'),         # GET + POST
    path('program-recommendations/', ProgramRecommendationListCreateView.as_view(), name='program-ai'),  # GET + POST
    path('performance-tracking/', PerformanceTrackingListCreateView.as_view(), name='performance-ai'),   # GET + POST
]
