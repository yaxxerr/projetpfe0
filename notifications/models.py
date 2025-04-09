from django.db import models

class Notification(models.Model):
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:30]}"
