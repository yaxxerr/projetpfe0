from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Speciality, Level, Module, Chapter
from .serializers import SpecialitySerializer, LevelSerializer,ResourceSerializer, ModuleSerializer, ChapterSerializer, UserSearchSerializer, ModuleSimpleSerializer, ChapterSimpleSerializer
from rest_framework import generics, permissions
from .models import Resource, AccessRequest
from .serializers import ResourceSerializer, AccessRequestSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from users.serializers import UserBasicSerializer

class ResourceSearchFlexibleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chapter_name = request.query_params.get("chapter")
        module_name = request.query_params.get("module")
        resource_type = request.query_params.get("type")

        if not resource_type:
            return Response({"error": "Please provide 'type' as a query parameter."}, status=400)

        if chapter_name:
            chapters = Chapter.objects.filter(name__icontains=chapter_name)
            resources = Resource.objects.filter(chapter__in=chapters, resource_type=resource_type)

        elif module_name:
            modules = Module.objects.filter(name__icontains=module_name)
            chapters = Chapter.objects.filter(module__in=modules)
            resources = Resource.objects.filter(chapter__in=chapters, resource_type=resource_type)

        else:
            return Response({"error": "Provide either 'chapter' or 'module' as a filter."}, status=400)

        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)


def index(request):
    return HttpResponse("Welcome to courses-endpoint")

# 🔹 GET + POST views
class SpecialityListCreateView(generics.ListCreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    permission_classes = [AllowAny]

class LevelListCreateView(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [AllowAny]

class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

class ModuleDetailView(RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [AllowAny]

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

# 🔍 Module Search View
class ModuleSearchView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSimpleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['speciality', 'level']
    search_fields = ['name']

# 🔍 Chapter Search View
class ChapterSearchView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSimpleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'module__name']

# 🔍 Resource Search Vie
class ResourceSearchView(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'resource_type', 'chapter__name']
