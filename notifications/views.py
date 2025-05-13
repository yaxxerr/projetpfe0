from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import  IsAuthenticated
from .models import Notification, Announcement
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AnnouncementSerializer
from users.models import User, Follow
from notifications.models import Notification

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


class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"detail": "✅ All notifications marked as read."})

class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_professor():
            raise PermissionDenied("Only professors can post announcements.")

        # Get filters
        level = self.request.data.get('level')
        speciality = self.request.data.get('speciality')

        announcement = serializer.save(owner=user, level=level, speciality=speciality)

        # Send notifications
        followers = Follow.objects.filter(professor=user).select_related("student")
        if level:
            followers = followers.filter(student__level=level)
        if speciality:
            followers = followers.filter(student__speciality=speciality)

        for follow in followers:
            Notification.objects.create(
                    recipient=follow.student,
                    message=f"📢 {announcement.title}: {announcement.content}",
                    type='announcement',
                    announcement=announcement  # 🔗 LINK IT!
)


class AnnouncementsByProfessorView(APIView):
    def get(self, request, professor_id):
        try:
            professor = User.objects.get(id=professor_id, user_type="professor")
        except User.DoesNotExist:
            return Response({"detail": "Professor not found."}, status=404)

        announcements = Announcement.objects.filter(owner=professor).order_by("-created_at")
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
