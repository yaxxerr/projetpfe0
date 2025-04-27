from django.http import HttpResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
import random
import requests
from django.conf import settings

from .models import (
    ChatbotMessage,
    GeneratedQuiz,
    ProgramRecommendation,
    PerformanceTracking
)
from .serializers import (
    ChatbotMessageSerializer,
    GeneratedQuizSerializer,
    ProgramRecommendationSerializer,
    PerformanceTrackingSerializer
)
from quizzes.models import Quiz, Question, Answer
from courses.models import Module

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"


def index(request): return HttpResponse("Welcome to Ai-endpoint")
def chatbot_messages_view(request): return HttpResponse("chatbot-messages-endpoint")
def generated_quizzes_view(request): return HttpResponse("generated-quizzes-endpoint")
def program_recommendations_view(request): return HttpResponse("program-recommendations-endpoint")
def performance_tracking_view(request): return HttpResponse("performance-tracking-endpoint")


# 💬 Chatbot messages using OpenRouter
class ChatbotMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_input = serializer.validated_data['user_message'].strip()
        bot_reply = self.generate_response_with_openrouter(user_input)
        serializer.save(user=self.request.user, bot_response=bot_reply)

    def generate_response_with_openrouter(self, prompt):
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            response = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"⚠️ AI Error: {str(e)}"


# 🧠 Auto-Generate Quiz (with AI-powered questions)
class GeneratedQuizListCreateView(generics.ListCreateAPIView):
    queryset = GeneratedQuiz.objects.all()
    serializer_class = GeneratedQuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        module = random.choice(Module.objects.all())

        quiz = Quiz.objects.create(
            title=f"AI Quiz for {module.name}",
            description="This quiz was generated with AI.",
            duration=20,
            module=module,
            type="qcm",
            created_by=user
        )

        # Call AI for questions
        try:
            prompt = f"Generate 3 QCM-style questions with 4 answers each for the topic: {module.name}. Indicate the correct answer index (0-based)."
            ai_response = self.query_ai(prompt)
            question_blocks = ai_response.strip().split("\n\n")

            for block in question_blocks:
                lines = block.strip().split("\n")
                question_text = lines[0]
                answers = lines[1:5]
                correct_index = int(lines[5].split(":")[-1].strip())

                q = Question.objects.create(quiz=quiz, texte=question_text, type="qcm")
                for idx, text in enumerate(answers):
                    Answer.objects.create(
                        question=q,
                        texte=text,
                        is_correct=(idx == correct_index)
                    )

        except Exception as e:
            Question.objects.create(quiz=quiz, texte=f"⚠️ Failed to generate with AI: {str(e)}", type="text")

        serializer.save(user=user, quiz=quiz)

    def query_ai(self, prompt):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        response = requests.post(OPENROUTER_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']


# 🎯 Program recommendations (kept simple)
class ProgramRecommendationListCreateView(generics.ListCreateAPIView):
    queryset = ProgramRecommendation.objects.all()
    serializer_class = ProgramRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        all_modules = list(Module.objects.all())
        random.shuffle(all_modules)

        recommended = all_modules[:3]
        program = serializer.save(user=user)
        program.recommended_modules.set(recommended)


# 📊 Performance tracking
class PerformanceTrackingListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceTracking.objects.all()
    serializer_class = PerformanceTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
