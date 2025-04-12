from django.urls import path
from .views import NotificationListView, NotificationMarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),                # GET /api/notifications/
    path('<int:pk>/read/', NotificationMarkAsReadView.as_view(), name='notification-read'),  # PATCH /api/notifications/1/read/
]
