# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Module, Level, Speciality

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    background = models.TextField(blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, blank=True)
    modules = models.ManyToManyField(Module, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_student() and self.level and self.speciality:
            modules = Module.objects.filter(level=self.level, speciality=self.speciality)
            self.modules.set(modules)

    def is_professor(self):
        return self.user_type == 'professor'

    def is_student(self):
        return self.user_type == 'student'

    def use_chatbot(self, message):
        from ai.models import ChatbotMessage
        response = "This is a dummy chatbot response"
        return ChatbotMessage.objects.create(
            user=self,
            user_message=message,
            bot_response=response
        )

class ProfessorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='professor')

class Professor(User):
    objects = ProfessorManager()

    class Meta:
        proxy = True

    def create_quiz(self, title, description, duration, module, quiz_type='qcm'):
        from quizzes.models import Quiz
        return Quiz.objects.create(
            title=title,
            description=description,
            duration=duration,
            module=module,
            type=quiz_type,
            created_by=self
        )

    def add_resource(self, name, res_type, link, chapter):
        from resources.models import Resource
        return Resource.objects.create(
            name=name,
            resource_type=res_type,
            link=link,
            chapter=chapter,
            owner=self
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
        from programs.models import Program
        program = Program.objects.create(student=self)
        return program

    def track_performance(self, strong_modules, weak_modules, time_on_platform):
        from ai.models import PerformanceTracking
        return PerformanceTracking.objects.create(
            user=self,
            strong_modules=strong_modules,
            weak_modules=weak_modules,
            platform_time=time_on_platform
        )