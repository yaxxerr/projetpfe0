from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizSubmission


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Quiz._meta.get_field('module').remote_field.model.objects.all())
    chapter = serializers.PrimaryKeyRelatedField(
        queryset=Quiz._meta.get_field('chapter').remote_field.model.objects.all(),
        allow_null=True, required=False
    )
    created_by = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    # ✅ Extra fields for display
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'duration', 'type',
            'module', 'chapter', 'created_by',
            'creation_mode', 'created_at', 'visibility', 'questions',
            'chapter_name', 'created_by_username'  # ✅ Include these
        ]


class QuizSubmissionSerializer(serializers.ModelSerializer):
    selected_answers = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        many=True
    )
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'student', 'selected_answers', 'submitted_at', 'score']
        read_only_fields = ['id', 'submitted_at', 'score', 'student']

