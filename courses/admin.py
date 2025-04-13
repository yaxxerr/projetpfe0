from django.contrib import admin
from .models import Speciality, Level, Module, Chapter, Resource

admin.site.register(Speciality)
admin.site.register(Level)
admin.site.register(Module)
admin.site.register(Chapter)
admin.site.register(Resource)