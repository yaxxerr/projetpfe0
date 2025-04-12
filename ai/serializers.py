from rest_framework import serializers
from .models import ChatbotMessage, GeneratedQuiz, ProgramRecommendation, PerformanceTracking
from courses.models import Module
from quizzes.models import Quiz


class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = '__all__'


class GeneratedQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedQuiz
        fields = '__all__'


class ProgramRecommendationSerializer(serializers.ModelSerializer):
    recommended_modules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Module.objects.all()
    )

    class Meta:
        model = ProgramRecommendation
        fields = '__all__'


class PerformanceTrackingSerializer(serializers.ModelSerializer):
    strong_modules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Module.objects.all()
    )
    weak_modules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Module.objects.all()
    )

    class Meta:
        model = PerformanceTracking
        fields = '__all__'
