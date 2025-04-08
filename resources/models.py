from django.db import models
from users.models import User
from courses.models import Chapter

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

class AccessRequest(models.Model):
    resource = models.ForeignKey(Resource, related_name='access_requests', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='resource_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=True)  # Null = pending, True = accepted, False = rejected

    def approve(self):
        self.approved = True
        self.save()

    def reject(self):
        self.approved = False
        self.save()

    def __str__(self):
        status = "Pending" if self.approved is None else "Accepted" if self.approved else "Rejected"
        return f"Request by {self.requester.username} for {self.resource.name} ({status})"
