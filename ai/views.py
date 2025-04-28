from django.http import HttpResponse
from rest_framework import generics, permissions
import requests
import random
import os

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

# Load environment variables or fallback values
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-real-api-key")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-4-maverick:free"

# --- Basic debug endpoints ---
def index(request):
    return HttpResponse("Welcome to the AI Endpoints 🎯")

def chatbot_messages_view(request):
    return HttpResponse("Chatbot Messages Endpoint 🔥")

def generated_quizzes_view(request):
    return HttpResponse("Generated Quizzes Endpoint 🧠")

def program_recommendations_view(request):
    return HttpResponse("Program Recommendations Endpoint 📚")

def performance_tracking_view(request):
    return HttpResponse("Performance Tracking Endpoint 📈")


# 💬 Chatbot API
class ChatbotMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_message = serializer.validated_data['user_message']
        bot_response = self.ask_openrouter(f"Answer clearly: {user_message}")
        serializer.save(user=self.request.user, bot_response=bot_response)

    def ask_openrouter(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful and knowledgeable educational assistant."},
                {"role": "user", "content": message},
            ],
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"[OpenRouter Chatbot Error] {e}")
            return "Error contacting AI service."


# 🧠 Quiz Generation API
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
            raise ValueError("Module and Chapters are required.")

        chapter_names = ", ".join([chapter.name for chapter in chapters])

        prompt = (
            f"Generate a 15-question {quiz_type.upper()} quiz for the module '{module.name}', "
            f"covering the chapters: {chapter_names}. "
            f"Difficulty: {difficulty}/5. "
            "For each question:\n"
            "- Write 'Q: [question text]'\n"
            "- Then write 4 options like '- Option text'\n"
            "- After the options, write 'Correct Answer: [number from 1 to 4]'\n"
            "Example:\n"
            "Q: What is the capital of France?\n"
            "- Berlin\n"
            "- Madrid\n"
            "- Paris\n"
            "- Rome\n"
            "Correct Answer: 3"
        )

        ai_response = self.ask_openrouter(prompt)

        quiz = Quiz.objects.create(
            title=f"Quiz for {module.name}",
            description=f"Auto-generated quiz covering {chapter_names} (Difficulty {difficulty})",
            duration=45,
            module=module,
            type=quiz_type,
            created_by=user,
            creation_mode='ai'
        )

        self.parse_questions(ai_response, quiz, quiz_type)
        serializer.save(user=user, quiz=quiz)

    def ask_openrouter(self, message):
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "You are an AI expert specialized in generating clean educational quizzes."},
                {"role": "user", "content": message},
            ],
        }
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print(f"[OpenRouter Quiz Error] {e}")
            return "Error generating quiz."

    def parse_questions(self, raw_text, quiz, quiz_type):
        lines = raw_text.strip().split("\n")
        current_question = None
        options = []
        correct_index = None

        for line in lines:
            line = line.strip()
            if line.lower().startswith("q"):
                if current_question and options:
                    self.create_question_and_answers(quiz, current_question, options, correct_index)
                current_question = line.split(":", 1)[-1].strip()
                options = []
                correct_index = None
            elif line.startswith("-"):
                options.append(line[1:].strip())
            elif "correct answer" in line.lower():
                try:
                    correct_index = int(line.strip().split(":")[-1].strip()) - 1
                except Exception as e:
                    print(f"Parsing correct answer failed: {e}")
                    correct_index = None

        # Save the last question
        if current_question and options:
            self.create_question_and_answers(quiz, current_question, options, correct_index)

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


# 🎯 Program Recommendation API
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


# 📊 Performance Tracking API
class PerformanceTrackingListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceTracking.objects.all()
    serializer_class = PerformanceTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
