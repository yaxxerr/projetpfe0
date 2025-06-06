import re
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


# 🧠 Resource Serializer with full access logic and user info


class ResourceSerializer(serializers.ModelSerializer):
    visible_link = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    access_approved = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            'id', 'chapter', 'name', 'resource_type', 'access_type', 'access_approved',
            'link', 'visible_link', 'created_at', 'owner', 'owner_username', 'owner_name'
        ]
        read_only_fields = ['owner', 'created_at', 'access_approved', 'owner_username', 'owner_name', 'visible_link']

    def validate_link(self, value):
        # Validation souple : accepte tout ce qui commence par un schéma suivi de "://"
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', value):
            return value
        raise serializers.ValidationError(
            "Entrez une URL valide commençant par un schéma (ex: http://, https://, file://, ftp://, mailto://, etc.)"
        )

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['owner'] = request.user
        return super().create(validated_data)

    def get_access_approved(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return AccessRequest.objects.filter(
            resource=obj,
            requester=user,
            approved=True
        ).exists()

    # Sert pour l'affichage, respectant l'accès utilisateur
    def get_visible_link(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if obj.access_type == 'public':
            return obj.link
        if user and user.is_authenticated:
            if obj.owner == user or AccessRequest.objects.filter(resource=obj, requester=user, approved=True).exists():
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
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            return []
        return ResourceSerializer(
            obj.resources.all(), many=True, context=self.context
        ).data

    def get_default_resources(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            return []
        return ResourceSerializer(
            obj.resources.filter(owner__is_superuser=True), many=True, context=self.context
        ).data

    def get_private_resources(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_authenticated:
            return []
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
