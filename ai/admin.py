from django.contrib import admin
from .models import Chatbot, QuizGenerator, ResumeBuilder, PerformanceTracker

admin.site.register(Chatbot)
admin.site.register(QuizGenerator)
admin.site.register(ResumeBuilder)
admin.site.register(PerformanceTracker)
