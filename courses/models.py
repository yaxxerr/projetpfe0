# courses/models.py

from django.db import models
from users.models import User, Level, Speciality

class Module(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(help_text="Module order")
    # A module can be associated with multiple levels and specialities.
    levels = models.ManyToManyField(Level, related_name='modules')
    specialities = models.ManyToManyField(Speciality, related_name='modules')

    def __str__(self):
        return self.title

class ModuleSubscription(models.Model):
    """
    Tracks both auto-assigned and manual subscriptions.
    When a student sets their level and speciality, modules matching those criteria
    can be auto-assigned (auto_assigned=True). Students may also manually subscribe.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_subscriptions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='subscriptions')
    auto_assigned = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} subscribed to {self.module.title}"

class Course(models.Model):
    # Each Course belongs to a Module.
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # The professor who creates the course.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    # Each Chapter belongs to a Course.
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(help_text="Chapter order within the course")

    def __str__(self):
        return self.title

class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
