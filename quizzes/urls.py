from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='quizzes-home'),
    # add other paths here
]