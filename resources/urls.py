from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='resources-home'),
    path('resources/', views.resource_view, name='resources-endpoint'),
    path('access-requests/', views.access_request_view, name='access-requests-endpoint'),
]