from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='resources-home'),

     path('resources/', views.ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource-detail'),

    path('access-requests/', views.AccessRequestListCreateView.as_view(), name='accessrequest-list-create'),
    path('access-requests/<int:pk>/', views.AccessRequestDetailView.as_view(), name='accessrequest-detail'),
]