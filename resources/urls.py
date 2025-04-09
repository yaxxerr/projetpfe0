from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='resources-home'),
    # add other paths here
]