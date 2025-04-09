from django.db import models

# Fixed: Avoid circular import
# Do not directly import User
from courses.models import Module
from quizzes.models import Quiz
from notifications.models import Notification

class Program(models.Model):
    student = models.ForeignKey('users.User', related_name='programs', on_delete=models.CASCADE)
    recommended_modules = models.ManyToManyField(Module, related_name='recommended_in_programs')
    modules_to_improve = models.ManyToManyField(Module, related_name='improve_in_programs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Program for {self.student.username} created on {self.created_at.date()}"

    @staticmethod
    def create_from_quiz_results(student, quiz_results):
        program = Program.objects.create(student=student)

        good_modules = []
        weak_modules = []

        for quiz, score in quiz_results.items():
            if score >= 75:  # threshold for good performance
                good_modules.append(quiz.module)
            else:
                weak_modules.append(quiz.module)

        program.recommended_modules.set(good_modules)
        program.modules_to_improve.set(weak_modules)

        # ✅ Notify the student about their personalized program
        Notification.objects.create(
            recipient=student,
            message="📘 A personalized program has been created for you based on your quiz results."
        )

        if weak_modules:
            module_names = ", ".join([mod.name for mod in weak_modules])
            Notification.objects.create(
                recipient=student,
                message=f"⚠️ Focus on improving these modules: {module_names}"
            )

        if good_modules:
            module_names = ", ".join([mod.name for mod in good_modules])
            Notification.objects.create(
                recipient=student,
                message=f"💪 Great job on: {module_names}. They're added to your recommended program."
            )

        return program
