from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='users-home'),
    path('users/', views.user_view, name='users-endpoint'),
    path('professors/', views.professor_view, name='professors-endpoint'),
    path('students/', views.student_view, name='students-endpoint'),
]