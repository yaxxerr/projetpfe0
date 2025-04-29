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
    PerformanceTrackingSerializer,
    StudyProgramRequestSerializer
)
from quizzes.models import Quiz, Question, Answer
from courses.models import Module, Chapter

# OpenRouter config
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-4-maverick:free"

# --- Basic debug endpoints ---
def index(request):
    return HttpResponse("Bienvenue aux Endpoints IA 🎯")

def chatbot_messages_view(request):
    return HttpResponse("Chatbot Messages Endpoint 🔥")

def generated_quizzes_view(request):
    return HttpResponse("Generated Quizzes Endpoint 🧠")

def program_recommendations_view(request):
    return HttpResponse("Program Recommendations Endpoint 📚")

def performance_tracking_view(request):
    return HttpResponse("Performance Tracking Endpoint 📈")

# 💬 Chatbot
class ChatbotMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_message = serializer.validated_data['user_message']
        bot_response = self.ask_openrouter(f"Réponds clairement en français : {user_message}")
        serializer.save(user=self.request.user, bot_response=bot_response)

    def ask_openrouter(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Tu es un assistant éducatif qui parle en français."},
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

# 🧠 Quiz Generator
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

        chapter_names = ", ".join([chapter.name for chapter in chapters])

        prompt = (
            f"Génère un quiz de 15 questions de type {quiz_type.upper()} sur le module '{module.name}', "
            f"couvrant les chapitres : {chapter_names}. Difficulté : {difficulty}/5.\n"
            "Format strict :\n"
            "Q: [question]\n"
            "- Option 1\n"
            "- Option 2\n"
            "- Option 3\n"
            "- Option 4\n"
            "Réponse correcte : [1-4]"
        )

        ai_response = self.ask_openrouter(prompt)
        print("=== RÉPONSE QUIZ IA ===")
        print(ai_response)
        print("=======================")

        quiz = Quiz.objects.create(
            title=f"Quiz pour {module.name}",
            description=f"Auto-généré pour {chapter_names} (Difficulté {difficulty})",
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
                {"role": "system", "content": "Tu es un expert pour créer des quiz éducatifs en français."},
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
                print(f"[Erreur Parse Quiz] {e}\nBLOCK:\n{block}")

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

# 📚 Program Recommandation (Générateur IA Personnalisé)
class ProgramRecommendationListCreateView(generics.CreateAPIView):
    serializer_class = StudyProgramRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        study_hours_per_day = request.data.get("study_hours_per_day")
        days_until_exam = request.data.get("days_until_exam")
        preferred_study_time = request.data.get("preferred_study_time")
        goals = request.data.get("goals")

        if not study_hours_per_day or not days_until_exam or not preferred_study_time or not goals:
            return HttpResponse("Tous les champs sont requis.", status=400)

        prompt = (
            f"En tant qu'expert éducatif, génère un programme d'étude personnalisé en français pour un étudiant :\n"
            f"- Temps d'étude par jour : {study_hours_per_day} heures\n"
            f"- Nombre de jours jusqu'aux examens : {days_until_exam} jours\n"
            f"- Préférence : {preferred_study_time}\n"
            f"- Objectifs : {goals}\n\n"
            "Le programme doit inclure :\n"
            "- Les modules à étudier par jour\n"
            "- Les chapitres spécifiques\n"
            "- Des suggestions de quiz\n"
            "- Conseils d'organisation\n"
            "Présente-le proprement, clair et motivant !"
        )

        study_program_text = self.ask_openrouter(prompt)

        # Save ProgramRecommendation
        program = ProgramRecommendation.objects.create(
            user=user,
            recommendation_text=study_program_text
        )

        return HttpResponse(study_program_text, content_type="text/plain")

    def ask_openrouter(self, prompt):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "Tu es un assistant spécialisé dans la planification éducative personnalisée."},
                {"role": "user", "content": prompt},
            ],
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"[Erreur OpenRouter Programme] {e}")
            return "Erreur lors de la création du programme."

# 📈 Performance Tracking
class PerformanceTrackingListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceTracking.objects.all()
    serializer_class = PerformanceTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
