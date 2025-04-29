from rest_framework import serializers
from .models import ChatbotMessage, GeneratedQuiz, ProgramRecommendation, PerformanceTracking
from courses.models import Module
from quizzes.models import Quiz
from courses.models import Module, Chapter

class GeneratedQuizSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        write_only=True
    )
    chapters = serializers.PrimaryKeyRelatedField(
        queryset=Chapter.objects.all(),
        many=True,
        write_only=True
    )
    difficulty = serializers.IntegerField(min_value=1, max_value=5, write_only=True)
    quiz_type = serializers.ChoiceField(
        choices=[('qcm', 'QCM'), ('free', 'Free Response')],
        write_only=True
    )

    class Meta:
        model = GeneratedQuiz
        fields = ['id', 'user', 'quiz', 'module', 'chapters', 'difficulty', 'quiz_type']
        read_only_fields = ['id', 'user', 'quiz']

    def create(self, validated_data):
        # Remove extra fields before creating the model instance
        validated_data.pop('module', None)
        validated_data.pop('chapters', None)
        validated_data.pop('difficulty', None)
        validated_data.pop('quiz_type', None)

        return super().create(validated_data)
class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = ['id', 'user_message', 'bot_response', 'timestamp', 'user']
        read_only_fields = ['bot_response', 'timestamp', 'user']



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
