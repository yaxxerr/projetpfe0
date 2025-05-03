from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import  IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

#GET
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

#PATCH
class NotificationMarkAsReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, is_read=False)

    def perform_update(self, serializer):
        serializer.instance.mark_as_read()

class MyAnnouncementsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            type='announcement'
        ).order_by('-created_at')


class AnnouncementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_professor():
            return Response({"detail": "Not allowed."}, status=403)

        message = request.data.get("message")
        if not message:
            return Response({"detail": "Message required."}, status=400)

        followers = request.user.followers.select_related('student')
        for f in followers:
            Notification.objects.create(
    recipient=f.student,
    message=f"📢 Announcement from {request.user.username}: {message}",
    type='announcement' 
)
        return Response({"detail": "Announcement sent."})

class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"detail": "✅ All notifications marked as read."})