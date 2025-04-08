from django.db import models

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

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.module.name})"
