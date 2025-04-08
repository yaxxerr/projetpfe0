from django.contrib import admin
from .models import ChatbotMessage, GeneratedQuiz, ProgramRecommendation, PerformanceTracking

admin.site.register(ChatbotMessage)
admin.site.register(GeneratedQuiz)
admin.site.register(ProgramRecommendation)
admin.site.register(PerformanceTracking)