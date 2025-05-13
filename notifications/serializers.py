from rest_framework import serializers
from .models import Notification , Announcement

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'recipient', 'created_at']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'owner']
        read_only_fields = ['owner', 'created_at']
