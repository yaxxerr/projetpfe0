from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('general', 'General'),
        ('announcement', 'Announcement'),
        # you can add more types if needed
    )

    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')  # <-- Add this

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:30]}"
