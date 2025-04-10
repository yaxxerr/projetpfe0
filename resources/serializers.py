from rest_framework import serializers
from .models import Resource, AccessRequest
from users.models import User
from courses.models import Chapter


class ResourceSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id',
            'name',
            'resource_type',
            'link',
            'access_type',
            'created_at',
            'owner',
            'owner_username',
            'chapter',
            'chapter_name',
        ]
        read_only_fields = ['created_at', 'owner_username', 'chapter_name']


class AccessRequestSerializer(serializers.ModelSerializer):
    requester_username = serializers.CharField(source='requester.username', read_only=True)
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = AccessRequest
        fields = [
            'id',
            'resource',
            'resource_name',
            'requester',
            'requester_username',
            'message',
            'created_at',
            'approved',
            'status',
        ]
        read_only_fields = ['created_at', 'status', 'resource_name', 'requester_username']

    def get_status(self, obj):
        if obj.approved is None:
            return 'Pending'
        return 'Accepted' if obj.approved else 'Rejected'
