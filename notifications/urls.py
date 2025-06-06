from django.urls import path
from .views import (
    CreateAnnouncementView,
    AnnouncementsByProfessorView,
    NotificationListView,
    MarkAllNotificationsReadView,
    MyAnnouncementsView,
    NotificationMarkAsReadView,
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),          
    path('my-announcements/', MyAnnouncementsView.as_view(), name='my-announcements'),
    path('<int:pk>/read/', NotificationMarkAsReadView.as_view(), name='notification-read'),  
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
    path('announce-create/', CreateAnnouncementView.as_view(), name='create-announcement'),
    path('by-professor/<int:professor_id>/', AnnouncementsByProfessorView.as_view(), name='professor-announcements'),
]
