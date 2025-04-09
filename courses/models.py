from django.db import models
from notifications.models import Notification

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
