from django.http import HttpResponse
from rest_framework import generics, permissions
import requests
import random
import os
import re

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
from courses.models import Module, Chapter

# Configuration OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-4-maverick:free"

# --- Endpoints de Debug ---
def index(request):
    return HttpResponse("Bienvenue aux Endpoints IA 🎯")

def chatbot_messages_view(request):
    return HttpResponse("Endpoint Chatbot 🔥")

def generated_quizzes_view(request):
    return HttpResponse("Endpoint Quiz Générés 🧠")

def program_recommendations_view(request):
    return HttpResponse("Endpoint Recommandations de Programmes 📚")

def performance_tracking_view(request):
    return HttpResponse("Endpoint Suivi de Performance 📈")

# 💬 Chatbot IA (Assistant)
class ChatbotMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_message = serializer.validated_data['user_message']
        bot_response = self.ask_openrouter(f"Réponds clairement et simplement en français : {user_message}")
        serializer.save(user=self.request.user, bot_response=bot_response)

    def ask_openrouter(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Tu es un assistant éducatif intelligent qui répond toujours en français."},
                {"role": "user", "content": message},
            ],
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"[Erreur OpenRouter Chatbot] {e}")
            return "Erreur de communication avec l'IA."

# 🧠 Générateur de Quiz IA
class GeneratedQuizListCreateView(generics.ListCreateAPIView):
    queryset = GeneratedQuiz.objects.all()
    serializer_class = GeneratedQuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        user = self.request.user
        module = validated_data['module']
        chapters = validated_data['chapters']
        difficulty = validated_data['difficulty']
        quiz_type = validated_data['quiz_type']

        if not module or not chapters:
            raise ValueError("Le module et les chapitres sont obligatoires.")

        chapter_names = ", ".join([chapter.name for chapter in chapters])

        prompt = (
            f"Génère un quiz de 15 questions de type {quiz_type.upper()} pour le module '{module.name}', "
            f"couvrant les chapitres suivants : {chapter_names}. "
            f"Niveau de difficulté : {difficulty}/5.\n"
            "**Format strict :**\n"
            "Q: [texte de la question]\n"
            "- Option 1\n"
            "- Option 2\n"
            "- Option 3\n"
            "- Option 4\n"
            "Réponse correcte : [numéro de l'option correcte entre 1 et 4]\n\n"
            "**Règles importantes :**\n"
            "- Commence chaque question par 'Q:'\n"
            "- Chaque option commence par '-'\n"
            "- Utilise 'Réponse correcte : [numéro]' pour donner la réponse correcte\n"
            "- Aucune numérotation ou lettre dans les options, juste '-'"
        )

        ai_response = self.ask_openrouter(prompt)
        print("=== RÉPONSE BRUTE IA ===")
        print(ai_response)
        print("========================")

        quiz = Quiz.objects.create(
            title=f"Quiz pour {module.name}",
            description=f"Quiz généré couvrant {chapter_names} (Difficulté {difficulty})",
            duration=45,
            module=module,
            type=quiz_type,
            created_by=user,
            creation_mode='ai'
        )

        self.parse_questions(ai_response, quiz)
        serializer.save(user=user, quiz=quiz)

    def ask_openrouter(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Tu es spécialisé dans la création de quiz éducatifs en français."},
                {"role": "user", "content": message},
            ],
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"[Erreur OpenRouter Quiz] {e}")
            return ""

    def parse_questions(self, raw_text, quiz):
        question_blocks = re.split(r"\nQ[:：]", raw_text)
        for block in question_blocks:
            block = block.strip()
            if not block:
                continue

            try:
                lines = block.split("\n")
                question_text = lines[0].strip()
                options = []
                correct_index = None

                for line in lines[1:]:
                    if line.startswith("-"):
                        options.append(line[1:].strip())
                    elif "réponse correcte" in line.lower():
                        match = re.search(r"(\d+)", line)
                        if match:
                            correct_index = int(match.group(1)) - 1

                if question_text and options:
                    self.create_question_and_answers(quiz, question_text, options, correct_index)
            except Exception as e:
                print(f"[Erreur Parse] {e}\nBLOCK:\n{block}")

    def create_question_and_answers(self, quiz, question_text, answers_list, correct_index):
        question = Question.objects.create(
            quiz=quiz,
            text=question_text
        )
        for idx, answer_text in enumerate(answers_list):
            Answer.objects.create(
                question=question,
                text=answer_text,
                is_correct=(idx == correct_index)
            )

# 📚 Recommandations de Programmes
class ProgramRecommendationListCreateView(generics.ListCreateAPIView):
    queryset = ProgramRecommendation.objects.all()
    serializer_class = ProgramRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        modules = list(Module.objects.all())
        random.shuffle(modules)
        recommended = modules[:3]
        program = serializer.save(user=user)
        program.recommended_modules.set(recommended)

# 📈 Suivi de Performance
class PerformanceTrackingListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceTracking.objects.all()
    serializer_class = PerformanceTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
