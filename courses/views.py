from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Speciality, Level, Module, Chapter
from .serializers import SpecialitySerializer, LevelSerializer, ModuleSerializer, ChapterSerializer, UserSearchSerializer
from rest_framework import generics, permissions
from .models import Resource, AccessRequest
from .serializers import ResourceSerializer, AccessRequestSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response


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
    permission_classes = [IsAuthenticated]


class AccessRequestListCreateView(generics.ListCreateAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [IsAuthenticated]

User = get_user_model()

class CourseSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response({
                "users": [],
                "modules": [],
                "levels": [],
                "specialities": []
            })

        users = User.objects.filter(username__icontains=query)[:5]
        modules = Module.objects.filter(name__icontains=query)[:5]
        levels = Level.objects.filter(name__icontains=query)[:5]
        specialities = Speciality.objects.filter(name__icontains=query)[:5]

        data = {
            "users": UserSearchSerializer(users, many=True).data,
            "modules": ModuleSerializer(modules, many=True).data,
            "levels": LevelSerializer(levels, many=True).data,
            "specialities": SpecialitySerializer(specialities, many=True).data,
        }
        return Response(data)
