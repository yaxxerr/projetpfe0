from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Speciality, Level, Module, Chapter
from .serializers import SpecialitySerializer, LevelSerializer, ModuleSerializer, ChapterSerializer
from rest_framework import generics, permissions
from .models import Resource, AccessRequest
from .serializers import ResourceSerializer, AccessRequestSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListAPIView


def index(request):
    return HttpResponse("Welcome to courses-endpoint")

# 🔹 GET + POST views
class SpecialityListCreateView(generics.ListCreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    permission_classes = [IsAuthenticated]

class LevelListCreateView(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAuthenticated]

class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

class ChapterListCreateView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated]


class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccessRequestListCreateView(generics.ListCreateAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


#get only
class SpecialityHierarchyView(ListAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer