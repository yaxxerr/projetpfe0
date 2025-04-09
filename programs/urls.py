from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='programs-home'),
    path('', views.program_view, name='programs-endpoint'),
]