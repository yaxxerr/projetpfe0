# resume/models.py

from django.db import models
from users.models import User

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Resume"

class ResumeSection(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(help_text="Section order in the resume")

    def __str__(self):
        return self.section_title

class ResumeField(models.Model):
    section = models.ForeignKey(ResumeSection, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} in {self.section.section_title}"
