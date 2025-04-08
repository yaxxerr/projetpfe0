# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Module

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    parcours = models.TextField(blank=True)
    level = models.ForeignKey('courses.Niveau', on_delete=models.SET_NULL, null=True, blank=True)
    specialty = models.ForeignKey('courses.Specialite', on_delete=models.SET_NULL, null=True, blank=True)
    modules = models.ManyToManyField(Module, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_student() and self.level and self.specialty:
            modules = Module.objects.filter(niveau=self.level, specialite=self.specialty)
            self.modules.set(modules)

    def is_professor(self):
        return self.user_type == 'professor'

    def is_student(self):
        return self.user_type == 'student'

    def use_chatbot(self, message):
        from ai.models import ChatbotMessage
        response = "This is a dummy chatbot response"
        return ChatbotMessage.objects.create(
            utilisateur=self,
            message_utilisateur=message,
            reponse_bot=response
        )

class ProfessorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='professor')

class Professor(User):
    objects = ProfessorManager()

    class Meta:
        proxy = True

    def create_quiz(self, title, description, duration, level, quiz_type='qcm'):
        from quizzes.models import Quiz
        return Quiz.objects.create(
            title=title,
            description=description,
            duration=duration,
            module=level,
            type=quiz_type,
            created_by=self
        )

    def add_resource(self, nom, res_type, lien, chapitre):
        from resources.models import Ressource
        return Ressource.objects.create(
            nom=nom,
            type=res_type,
            lien=lien,
            chapitre=chapitre,
            proprietaire=self
        )

class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='student')

class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def pass_quiz(self, quiz, answers):
        from quizzes.models import QuizAttempt
        score = 0  # Replace with actual quiz scoring logic
        return QuizAttempt.objects.create(
            student=self,
            quiz=quiz,
            score=score
        )

    def create_program(self):
        from programs.models import Programme
        programme = Programme.objects.create(utilisateur=self)
        return programme

    def track_performance(self, modules_bien, modules_faibles, temps_en_plateforme):
        from ai.models import Performance
        return Performance.objects.create(
            utilisateur=self,
            modules_bien=modules_bien,
            modules_faibles=modules_faibles,
            temps_en_plateforme=temps_en_plateforme
        )