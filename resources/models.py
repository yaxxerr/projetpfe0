from django.db import models
from users.models import User
from courses.models import Chapter
from notifications.models import Notification

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('pdf', 'PDF Document'),
        ('video', 'Video'),
    )

    ACCESS_TYPE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    link = models.URLField()
    chapter = models.ForeignKey(Chapter, related_name='resources', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owned_resources', on_delete=models.CASCADE)
    access_type = models.CharField(max_length=10, choices=ACCESS_TYPE_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_access_type_display()})"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            Notification.objects.create(
                recipient=self.owner,
                message=f"Your resource '{self.name}' was successfully published."
            )

            # Suggest this resource to other students (public only)
            if self.access_type == 'public':
                students = User.objects.filter(user_type='student')
                for student in students:
                    Notification.objects.create(
                        recipient=student,
                        message=f"New resource '{self.name}' is available for the chapter '{self.chapter.name}'."
                    )


class AccessRequest(models.Model):
    resource = models.ForeignKey(Resource, related_name='access_requests', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='resource_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=True)  # None = pending, True = approved, False = rejected

    def __str__(self):
        status = "Pending" if self.approved is None else "Accepted" if self.approved else "Rejected"
        return f"Request by {self.requester.username} for '{self.resource.name}' ({status})"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            Notification.objects.create(
                recipient=self.resource.owner,
                message=f"{self.requester.username} requested access to your private resource: '{self.resource.name}'."
            )

    def approve(self):
        self.approved = True
        self.save()

        Notification.objects.create(
            recipient=self.requester,
            message=f"✅ Your access request for '{self.resource.name}' has been approved!"
        )

    def reject(self):
        self.approved = False
        self.save()

        Notification.objects.create(
            recipient=self.requester,
            message=f"❌ Your access request for '{self.resource.name}' was rejected by {self.resource.owner.username}."
        )
