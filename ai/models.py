# ai/models.py
from django.db import models

class BaseAIModel(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} (v{self.version})"

class Chatbot(BaseAIModel):
    # Additional fields for the chatbot if needed
    pass

class QuizGenerator(BaseAIModel):
    # Additional fields for the quiz generator if needed
    pass

class ResumeBuilder(BaseAIModel):
    # Additional fields for the resume builder if needed
    pass

class PerformanceTracker(BaseAIModel):
    # Additional fields for performance tracking if needed
    pass
