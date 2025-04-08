from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'level', 'specialty')
    list_filter = ('user_type', 'level', 'specialty')
    search_fields = ('username', 'email')