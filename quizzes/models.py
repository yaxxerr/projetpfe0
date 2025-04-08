# quizzes/models.py
from django.db import models
from users.models import User
from courses.models import Module, Chapter

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = (
        ('qcm', 'Multiple Choice (QCM)'),
        ('free', 'Free Answer'),
    )

    CREATION_MODE_CHOICES = (
        ('manual', 'Created Manually'),
        ('ai', 'Created by AI'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES, default='qcm')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    creation_mode = models.CharField(max_length=10, choices=CREATION_MODE_CHOICES, default='manual')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def calculate_score(self, user_answers):
        score = 0
        for question in self.questions.all():
            correct_answers = question['answers'].filter(is_correct=True)
            correct_ids = set(ans.id for ans in correct_answers)
            user_ids = set(user_answers.get(str(question['id']), []))
            if correct_ids == user_ids:
                score += 1
        return score


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
