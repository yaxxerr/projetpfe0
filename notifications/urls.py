from django.urls import path
from .views import NotificationListView,MarkAllNotificationsReadView, MyAnnouncementsView, AnnouncementView, NotificationMarkAsReadView,MyAnnouncementsView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),   
    path('announce/', AnnouncementView.as_view(), name='professor-announce'),           
    path('my-announcements/', MyAnnouncementsView.as_view(), name='my-announcements'),
    path('<int:pk>/read/', NotificationMarkAsReadView.as_view(), name='notification-read'),  
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
]
