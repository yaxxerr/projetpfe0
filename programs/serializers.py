# programs/serializers.py

from rest_framework import serializers
from .models import Program
from courses.models import Module
from users.models import User

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'level', 'speciality']

class ProgramSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    recommended_modules = ModuleSerializer(many=True, read_only=True)
    modules_to_improve = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'student', 'recommended_modules', 'modules_to_improve', 'created_at']
