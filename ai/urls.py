from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ai-home'),
    path('chatbot-messages/', views.chatbot_messages_view, name='chatbot-messages'),
    path('generated-quizzes/', views.generated_quizzes_view, name='generated-quizzes'),
    path('program-recommendations/', views.program_recommendations_view, name='program-recommendations'),
    path('performance-tracking/', views.performance_tracking_view, name='performance-tracking'),
]
