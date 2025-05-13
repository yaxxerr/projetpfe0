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



class StudyProgramRequestSerializer(serializers.Serializer):
    study_hours_per_day = serializers.IntegerField(
        min_value=1, max_value=24,
        help_text="Nombre d'heures d'étude par jour"
    )
    days_until_exam = serializers.IntegerField(
        min_value=1,
        help_text="Nombre de jours restants avant les examens"
    )
    preferred_study_time = serializers.ChoiceField(
        choices=[('morning', 'Matin'), ('afternoon', 'Après-midi'), ('evening', 'Soir')],
        help_text="Moment préféré pour étudier"
    )
    goals = serializers.CharField(
        max_length=500,
        help_text="Objectifs de l'étudiant (ex: passer l'examen, être dans le top 10%)"
    )

class ProgramRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramRecommendation
        fields = ['id', 'user', 'recommendation_text', 'created_at']
        read_only_fields = ['id', 'user', 'recommendation_text', 'created_at']
class PerformanceTrackingSerializer(serializers.ModelSerializer):
    strong_modules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Module.objects.all(), required=False
    )
    weak_modules = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Module.objects.all(), required=False
    )
    average_score = serializers.FloatField(read_only=True)
    platform_time = serializers.IntegerField(read_only=True)  # in minutes
    feedback = serializers.CharField(read_only=True)

    class Meta:
        model = PerformanceTracking
        fields = [
            'id', 'user', 'strong_modules', 'weak_modules',
            'average_score', 'platform_time', 'feedback'
        ]
        read_only_fields = ['id', 'user', 'average_score', 'platform_time', 'feedback']
