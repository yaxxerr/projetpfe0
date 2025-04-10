from django.urls import path
from . import views
from .views import user_list, user_detail, register_user

urlpatterns = [
    path('', views.index, name='users-home'),
    path('users/', views.user_view, name='users-endpoint'),
    path('professors/', views.professor_view, name='professors-endpoint'),
    path('students/', views.student_view, name='students-endpoint'),

    path('all/', user_list, name='user-list'),
    path('<int:pk>/', user_detail, name='user-detail'),
    path('register/', register_user, name='user-register'),
]
