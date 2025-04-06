# resources/models.py

from django.db import models
from courses.models import Module, Chapter
from users.models import User

RESOURCE_TYPE_CHOICES = (
    ('pdf', 'PDF'),
    ('video', 'Video'),
    # Extend with other types if needed.
)

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    file_url = models.URLField(max_length=500, help_text="Google Drive URL to the resource")
    is_public = models.BooleanField(default=True, help_text="Set to False if the resource is private")
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resources_added',
        help_text="The professor who added this resource"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # The resource can be attached to a module (general resource) or a chapter (specific content).
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)

    def __str__(self):
        return self.title

class ResourceAccessRequest(models.Model):
    """
    Tracks a student's request for a private resource.
    The owner (professor) of the resource can accept or reject the request.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='access_requests')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    response_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.student.username} for {self.resource.title} [{self.status}]"
