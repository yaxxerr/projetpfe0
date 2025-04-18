from django.db import models
from notifications.models import Notification
from users.models import User

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.speciality.name} - {self.level.name})"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            from users.models import User  # ⬅️ Moved import here to avoid circular dependency
            professors = User.objects.filter(user_type='professor')
            for prof in professors:
                Notification.objects.create(
                    recipient=prof,
                    message=f"📘 A new module '{self.name}' has been added for {self.level.name} / {self.speciality.name}."
                )


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.module.name})"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            from users.models import User  # ⬅️ Local import to prevent circular crash
            students = User.objects.filter(user_type='student', modules=self.module)
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    message=f"🧩 A new chapter '{self.name}' has been added to your module: {self.module.name}."
                )


class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('cours-pdf', 'cours-pdf'),
        ('cours-video', 'cours-video'),
        ('td-pdf', 'td-pdf'),
        ('td-video', 'td-video'),
        ('tp-pdf', 'tp-pdf'),
        ('tp-video', 'tp-video')
    )

    ACCESS_TYPE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )

    name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    link = models.URLField()
    chapter = models.ForeignKey('Chapter', related_name='resources', on_delete=models.CASCADE)
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
    approved = models.BooleanField(null=True)  # None = pending

    def approve(self):
        self.approved = True
        self.save()

    def reject(self):
        self.approved = False
        self.save()

    def __str__(self):
        status = "Pending" if self.approved is None else "Accepted" if self.approved else "Rejected"
        return f"Request by {self.requester.username} for {self.resource.name} ({status})"
