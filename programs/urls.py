from django.urls import path
from . import views
from rest_framework import generics, permissions
from .models import Program
from .serializers import ProgramSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .views import ProgramListCreateView, MyProgramsListView

urlpatterns = [
    path('', ProgramListCreateView.as_view(), name='programs-all'),         # /api/programs/ → GET + POST
    path('my-programs/', MyProgramsListView.as_view(), name='my-programs'),    
]