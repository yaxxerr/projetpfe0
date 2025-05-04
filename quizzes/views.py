from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, QuizSubmission
from .serializers import QuizSerializer, QuizSubmissionSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuizSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

# ✅ GET: List all quizzes
# ✅ POST: Create a new quiz
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

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
        submission = serializer.save()
        submission.calculate_score()

# ✅ GET: List all quiz submissions
class QuizSubmissionListView(generics.ListAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]


class QuizSubmissionListCreateView(generics.ListCreateAPIView):
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

