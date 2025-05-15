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

# 🧠 Resource Serializer (for listing resources)
class ResourceSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    access_approved = serializers.SerializerMethodField()

    class Meta:
        model = Resource
<<<<<<< Updated upstream
        fields = [
            'id', 'chapter', 'name', 'resource_type', 'access_type', 'access_approved' ,
            'link', 'created_at', 'owner', 'owner_username', 'owner_name'
        ]
        read_only_fields = ['owner', 'created_at','access_approved', 'owner_username', 'owner_name']
=======
        fields = ['id', 'chapter', 'name', 'resource_type', 'access_type', 'link', 'created_at', 'owner_username', 'owner', 'owner_name']
        read_only_fields = ['owner', 'created_at', 'id', 'owner_username']
>>>>>>> Stashed changes

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
        return super().create(validated_data)

    def get_access_approved(self, obj):
        user = self.context['request'].user
        return AccessRequest.objects.filter(
            resource=obj,
            requester=user,
            approved=True
        ).exists()

    def get_link(self, obj):
        user = self.context['request'].user
        if obj.access_type == 'public':
            return obj.link
        if user.is_authenticated and obj.owner == user:
            return obj.link
        if user.is_authenticated and AccessRequest.objects.filter(resource=obj, requester=user, approved=True).exists():
            return obj.link
        return None

    def get_owner_name(self, obj):
        return obj.owner.username if obj.owner else None

# 🔍 For student/professor search bars
class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']

# 🔗 Access request serializer
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

# 📦 Chapter serializer (with nested resource views)
class ChapterSerializer(serializers.ModelSerializer):
    all_resources = serializers.SerializerMethodField()
    default_resources = serializers.SerializerMethodField()
    private_resources = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'module', 'all_resources', 'default_resources', 'private_resources']

    def get_all_resources(self, obj):
        return ResourceSerializer(
            obj.resources.all(), many=True, context=self.context
        ).data

    def get_default_resources(self, obj):
        return ResourceSerializer(
            obj.resources.filter(owner__is_superuser=True), many=True, context=self.context
        ).data

    def get_private_resources(self, obj):
        return ResourceSerializer(
            obj.resources.filter(access_type='private'), many=True, context=self.context
        ).data

# 📘 Module serializer (with chapters)
class ModuleSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'speciality', 'level', 'chapters']

# 🎓 Level serializer (with modules)
class LevelSerializer(serializers.ModelSerializer):
    module_set = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'name', 'description', 'module_set']

# 🧠 Speciality serializer (with levels)
class SpecialitySerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True, source='level_set')

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'levels']
