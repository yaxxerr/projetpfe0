from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='courses-home'),
    path('specialities/', views.speciality_view, name='speciality-endpoint'),
    path('levels/', views.level_view, name='level-endpoint'),
    path('modules/', views.module_view, name='module-endpoint'),
    path('chapters/', views.chapter_view, name='chapter-endpoint'),
]
