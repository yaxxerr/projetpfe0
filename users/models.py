# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Specialities"

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    # Inherits basic fields from AbstractUser.
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="User's area of expertise"
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="User's level (e.g., beginner, intermediate, advanced)"
    )
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username


