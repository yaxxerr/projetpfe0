# quizzes/serializers.py
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
    # Accept module and chapter as IDs in write operations, but show names in read
    module = serializers.PrimaryKeyRelatedField(queryset=Quiz._meta.get_field('module').remote_field.model.objects.all())
    chapter = serializers.PrimaryKeyRelatedField(
        queryset=Quiz._meta.get_field('chapter').remote_field.model.objects.all(),
        allow_null=True, required=False
    )
    created_by = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'duration', 'type',
            'module', 'chapter', 'created_by',
            'creation_mode', 'created_at', 'visibility', 'questions'
        ]


class QuizSubmissionSerializer(serializers.ModelSerializer):
    selected_answers = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        many=True
    )

    class Meta:
        model = QuizSubmission
        fields = ['id', 'quiz', 'student', 'selected_answers', 'submitted_at', 'score']
        read_only_fields = ['id', 'submitted_at', 'score']
