from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, QuizSubmission, Question, Answer
from .serializers import QuizSerializer, QuizSubmissionSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuizSerializer

class QuizFilteredListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Quiz.objects.all()
        chapter_id = self.request.query_params.get('chapter')
        module_id = self.request.query_params.get('module')

        if chapter_id:
            queryset = queryset.filter(chapter__id=chapter_id)
        elif module_id:
            queryset = queryset.filter(module__id=module_id)

        return queryset



# 🔍 Full CRUD for Quizzes
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# ✅ GET: List all quizzes | POST: Create a new quiz
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ✅ GET: Retrieve a single quiz by ID
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]


# ✅ POST: Submit answers for a quiz
class QuizSubmissionCreateView(generics.CreateAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        submission = serializer.save(student=self.request.user)
        submission.calculate_score()


# ✅ GET: List all quiz submissions
class QuizSubmissionListView(generics.ListAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]


# ✅ Combined: List + Create submissions
class QuizSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]


# ✅ POST a question to a quiz
class QuizQuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_id'])
        serializer.save(quiz=quiz)


# ✅ POST an answer to a question
class QuestionAnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        serializer.save(question=question)
