from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('student', 'created_at')
    filter_horizontal = ('recommended_modules', 'modules_to_improve')