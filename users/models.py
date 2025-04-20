from django.contrib.auth.models import AbstractUser
from django.db import models
from notifications.models import Notification

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    background = models.TextField(blank=True)
    modules = models.ManyToManyField('courses.Module', blank=True)
    speciality = models.ForeignKey('courses.Speciality', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey('courses.Level', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

    def is_professor(self):
        return self.user_type == 'professor'

    def is_student(self):
        return self.user_type == 'student'

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            Notification.objects.create(
                recipient=self,
                message="👋 Welcome to the platform! Your profile has been successfully created."
            )

    def assign_modules_to_student(self):
        if self.is_student() and self.level and self.speciality:
            from courses.models import Module  # Avoid circular import
            modules = Module.objects.filter(level=self.level, speciality=self.speciality)
            self.modules.set(modules)

            Notification.objects.create(
                recipient=self,
                message="📘 Modules have been assigned based on your level and speciality."
            )

            if modules.exists():
                Notification.objects.create(
                    recipient=self,
                    message=f"📘 Start with: {modules.first().name}"
                )
            else:
                Notification.objects.create(
                    recipient=self,
                    message="⚠️ No modules found for your profile. Please contact the admin."
                )


    def use_chatbot(self, message):
        from ai.models import ChatbotMessage
        response = "This is a dummy chatbot response"
        msg = ChatbotMessage.objects.create(
            user=self,
            user_message=message,
            bot_response=response
        )
        Notification.objects.create(
            recipient=self,
            message="💬 You received a new chatbot response."
        )
        return msg


class ProfessorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='professor')


class Professor(User):
    objects = ProfessorManager()

    class Meta:
        proxy = True

    def create_quiz(self, title, description, duration, module, quiz_type='qcm'):
        from quizzes.models import Quiz
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            duration=duration,
            module=module,
            type=quiz_type,
            created_by=self
        )
        Notification.objects.create(
            recipient=self,
            message=f"📝 Quiz '{title}' created successfully."
        )
        return quiz

    def add_resource(self, name, res_type, link, chapter):
        from courses.models import Resource
        res = Resource.objects.create(
            name=name,
            resource_type=res_type,
            link=link,
            chapter=chapter,
            owner=self
        )
        Notification.objects.create(
            recipient=self,
            message=f"📎 Resource '{name}' was added."
        )
        from .models import Follow
        followers = Follow.objects.filter(professor=self)
        for follow in followers:
            Notification.objects.create(
                recipient=follow.student,
                message=f"📥 {self.username} just posted a new resource: {name}"
            )
        return res


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='student')


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def pass_quiz(self, quiz, answers):
        from quizzes.models import QuizAttempt
        score = 0  # Placeholder: your quiz logic should calculate score properly
        attempt = QuizAttempt.objects.create(
            student=self,
            quiz=quiz,
            score=score
        )
        Notification.objects.create(
            recipient=self,
            message=f"✅ You completed quiz '{quiz.title}'. Your score: {score}%"
        )
        return attempt

    def create_program(self):
        from programs.models import Program
        program = Program.objects.create(student=self)
        Notification.objects.create(
            recipient=self,
            message="📘 A new learning program has been created for you."
        )
        return program

    def track_performance(self, strong_modules, weak_modules, time_on_platform):
        from ai.models import PerformanceTracking
        perf = PerformanceTracking.objects.create(
            user=self,
            platform_time=time_on_platform
        )
        perf.strong_modules.set(strong_modules)
        perf.weak_modules.set(weak_modules)
        Notification.objects.create(
            recipient=self,
            message="📊 Your performance has been recorded."
        )
        return perf


class Follow(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'professor')

    def __str__(self):
        return f"{self.student.username} follows {self.professor.username}"
