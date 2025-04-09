from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='programs-home'),
    # add other paths here
]