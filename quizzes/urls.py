from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='quizzes-home'),
    path('quizzes/', views.quiz_view, name='quizzes-endpoint'),
    path('questions/', views.question_view, name='questions-endpoint'),
    path('answers/', views.answer_view, name='answers-endpoint'),
]