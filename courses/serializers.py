from rest_framework import serializers
from .models import (
    Resource,
    AccessRequest,
    Speciality,
    Level,
    Module,
    Chapter
)
from django.contrib.auth import get_user_model

User = get_user_model()

# 🧠 Resource Serializer with extra info
class ResourceSerializer(serializers.ModelSerializer):
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    module_name = serializers.CharField(source='chapter.module.name', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id',
            'name',
            'resource_type',
            'access_type',
            'link',
            'chapter',
            'chapter_name',
            'module_name',
            'owner',
            'owner_username',
            'created_at'
        ]

# 🔍 For student search bar etc
class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

# 🔗 Resource request serializer
class AccessRequestSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if obj.approved is True:
            return "approved"
        elif obj.approved is False:
            return "rejected"
        return "pending"

    class Meta:
        model = AccessRequest
        fields = [
            'id',
            'resource',
            'resource_name',
            'requester',
            'requester_username',
            'message',
            'approved',
            'status',
            'created_at'
        ]

# 🧩 Nested Chapter > Resources
class ChapterSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'module', 'resources']

# 🧱 Nested Module > Chapters
class ModuleSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'speciality', 'level', 'chapters']

# 📚 Level includes its modules
class LevelSerializer(serializers.ModelSerializer):
    module_set = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'name', 'description', 'module_set']

# 🧠 Speciality > Levels
class SpecialitySerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True, source='level_set')

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'levels']
