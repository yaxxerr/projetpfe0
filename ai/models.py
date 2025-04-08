# ai/models.py
from django.db import models
from users.models import User
from quizzes.models import Quiz
from courses.models import Module

class ChatbotMessage(models.Model):
    user = models.ForeignKey(User, related_name='chatbot_messages', on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"


class GeneratedQuiz(models.Model):
    user = models.ForeignKey(User, related_name='generated_quizzes', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz '{self.quiz.title}' generated for {self.user.username}"


class ProgramRecommendation(models.Model):
    user = models.ForeignKey(User, related_name='program_recommendations', on_delete=models.CASCADE)
    recommended_modules = models.ManyToManyField(Module)
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Program recommendation for {self.user.username}"


class PerformanceTracking(models.Model):
    user = models.ForeignKey(User, related_name='performance_trackings', on_delete=models.CASCADE)
    strong_modules = models.ManyToManyField(Module, related_name='strong_in')
    weak_modules = models.ManyToManyField(Module, related_name='weak_in')
    platform_time = models.DurationField()
    tracked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance tracking for {self.user.username} at {self.tracked_at}"
