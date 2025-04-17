from rest_framework import serializers
from .models import Resource, AccessRequest
from .models import Speciality, Level, Module, Chapter, Resource
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'resources']

class ModuleSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'chapters']

class LevelSerializer(serializers.ModelSerializer):
    module_set = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'name', 'description', 'module_set']

class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = '__all__'

class SpecialitySerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True, source='level_set')

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'levels']