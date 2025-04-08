# programs/models.py
from django.db import models
from users.models import User
from courses.models import Module
from quizzes.models import Quiz

class Program(models.Model):
    student = models.ForeignKey(User, related_name='programs', on_delete=models.CASCADE)
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

        return program
