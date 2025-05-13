from django.urls import path
from . import views
from .views import (
    ChatbotMessageListCreateView,
    GeneratedQuizListCreateView,
    ProgramRecommendationListCreateView,
    PerformanceStatsView,
    UserProgramRecommendationListView,
)

urlpatterns = [
    path('', views.index, name='ai-home'),
    path('chatbot/', ChatbotMessageListCreateView.as_view(), name='chatbot-messages'),                   # GET + POST
    path('genquizzes/', GeneratedQuizListCreateView.as_view(), name='generated-quizzes'),         # GET + POST
    path('program-recommendations/', ProgramRecommendationListCreateView.as_view(), name='program-ai'),  # GET + POST
    path('user/<int:user_id>/program-recommendations/', UserProgramRecommendationListView.as_view(), name='user-program-recommendations'),
    path('performance/', PerformanceStatsView.as_view(), name='performance-stats'),
   
]
