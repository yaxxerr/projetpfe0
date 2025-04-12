from . import views
from .views import QuizViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizListCreateView, QuizSubmissionListCreateView
from .views import (
    QuizListCreateView,
    QuizDetailView,
    QuizSubmissionCreateView,
    QuizSubmissionListView
)

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('submissions/', QuizSubmissionListCreateView.as_view(), name='quiz-submission-list-create'),
    path('questions/', views.question_view, name='questions-endpoint'),
    path('answers/', views.answer_view, name='answers-endpoint'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('', QuizListCreateView.as_view(), name='quiz-list-create'),
    
    
]
