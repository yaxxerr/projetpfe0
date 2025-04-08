from django.contrib import admin
from .models import Resource, AccessRequest

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'access_type', 'chapter', 'owner', 'created_at')
    list_filter = ('resource_type', 'access_type')
    search_fields = ('name', 'chapter__name')

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ('resource', 'requester', 'approved', 'created_at')
    list_filter = ('approved',)