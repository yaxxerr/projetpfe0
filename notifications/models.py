from django.db import models
from django.conf import settings  # ✅ Only change

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('general', 'General'),
        ('announcement', 'Announcement'),
    )

    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')  # Leave this as-is
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:30]}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="announcements")
   
    # 🎯 NEW FILTER FIELDS
    level = models.CharField(max_length=50, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"

