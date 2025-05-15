from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet,
    QuizListCreateView,
    QuizDetailView,
    QuizSubmissionCreateView,
    QuizSubmissionListView,
    QuizSubmissionListCreateView,
    QuizQuestionCreateView,
    QuizFilteredListView,
    QuestionAnswerCreateView,
)

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('submissions/', QuizSubmissionListCreateView.as_view(), name='quiz-submission-list-create'),
    path('submissions/create/', QuizSubmissionCreateView.as_view(), name='quiz-submission-create'),
    path('<int:quiz_id>/questions/', QuizQuestionCreateView.as_view(), name='quiz-question-create'),
    path('filtered/', QuizFilteredListView.as_view(), name='quiz-filtered'),
    path('<int:quiz_id>/questions/<int:question_id>/answers/', QuestionAnswerCreateView.as_view(), name='question-answer-create'),
    path('', include(router.urls)),  # Include ViewSet routes
]
