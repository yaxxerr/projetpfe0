from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('quiz-generator/', views.quiz_generator_view, name='quiz_generator'),
    path('resume-builder/', views.resume_builder_view, name='resume_builder'),
    path('performance-tracker/', views.performance_tracker_view, name='performance_tracker'),
]
