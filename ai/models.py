from django.db import models
from users.models import User
from quizzes.models import Quiz
from courses.models import Module
from notifications.models import Notification
from datetime import timedelta


class ChatbotMessage(models.Model):
    user = models.ForeignKey(User, related_name='chatbot_messages', on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            Notification.objects.create(
                recipient=self.user,
                message="💬 The AI chatbot has replied to your message."
            )


class GeneratedQuiz(models.Model):
    user = models.ForeignKey(User, related_name='generated_quizzes', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz '{self.quiz.title}' generated for {self.user.username}"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            Notification.objects.create(
                recipient=self.user,
                message=f"🧠 A quiz titled '{self.quiz.title}' was generated based on your learning progress."
            )


from django.db import models
from users.models import User
from courses.models import Module, Chapter
from notifications.models import Notification

class ProgramRecommendation(models.Model):
    user = models.ForeignKey(User, related_name='program_recommendations', on_delete=models.CASCADE)
    recommendation_text = models.TextField(blank=True)
    recommended_modules = models.ManyToManyField(Module, blank=True)
    recommended_chapters = models.ManyToManyField(Chapter, blank=True)
    goals_per_day = models.JSONField(default=list, blank=True)  # 🧠 JSON List like [{'day': 1, 'goal': 'Study chapter 1'}, ...]
    completion_percentage = models.FloatField(default=0.0)  # 📈 % of completion
    recommended_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Program recommendation for {self.user.username}"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            modules = ", ".join([m.name for m in self.recommended_modules.all()])
            Notification.objects.create(
                recipient=self.user,
                message=f"📘 A new AI-powered study program has been created for you. Focus on: {modules}."
            )

            first_module = self.recommended_modules.first()
            if first_module:
                Notification.objects.create(
                    recipient=self.user,
                    message=f"👉 Start with module: {first_module.name}"
                )



class InitialModuleRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initial_ratings")
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    note = models.TextField(blank=True)
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.username} rated {self.module.name}: {self.rating}"


class PerformanceTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='detailed_performance')
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    quiz_average_score = models.FloatField(default=0.0)
    study_time = models.DurationField(default=0)
    self_assessment = models.TextField(blank=True)
    ai_feedback = models.TextField(blank=True)
    progress_score = models.FloatField(default=0.0)  # AI-generated
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Performance for {self.user.username} in {self.module.name}"