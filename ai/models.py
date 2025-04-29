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



class PerformanceTracking(models.Model):
    user = models.ForeignKey(User, related_name='performance_trackings', on_delete=models.CASCADE)
    strong_modules = models.ManyToManyField(Module, related_name='strong_in')
    weak_modules = models.ManyToManyField(Module, related_name='weak_in')
    platform_time = models.DurationField()
    tracked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance for {self.user.username} at {self.tracked_at}"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            total_minutes = round(self.platform_time.total_seconds() / 60)

            Notification.objects.create(
                recipient=self.user,
                message=f"📊 Performance updated. You spent {total_minutes} minutes on the platform today."
            )

            weak = self.weak_modules.all()
            if weak.exists():
                weak_list = ", ".join([m.name for m in weak])
                Notification.objects.create(
                    recipient=self.user,
                    message=f"⚠️ You’re struggling with: {weak_list}. Review these modules or try a practice quiz."
                )

            strong = self.strong_modules.all()
            if strong.exists():
                strong_list = ", ".join([m.name for m in strong])
                Notification.objects.create(
                    recipient=self.user,
                    message=f"💪 You're doing great in: {strong_list}. Keep it up!"
                )
