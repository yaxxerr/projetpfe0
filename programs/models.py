# programs/models.py

from django.db import models
from users.models import User
from courses.models import Module

class Program(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='programs_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProgramModule(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_modules')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='program_modules')
    order = models.PositiveIntegerField(help_text="Module order in the program")

    def __str__(self):
        return f"{self.program.title} - {self.module.title}"

class ProgramProgress(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_progress')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                   help_text="Progress in percentage")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress in {self.program.title}"
