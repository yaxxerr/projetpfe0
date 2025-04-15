from rest_framework import serializers
from .models import Resource, AccessRequest
from .models import Speciality, Level, Module, Chapter, Resource

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

class SpecialityHierarchySerializer(serializers.ModelSerializer):
    level_set = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'level_set']


class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = '__all__'

class SpecialitySerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True, source='level_set')

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'levels']