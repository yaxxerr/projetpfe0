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
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from users.serializers import UserBasicSerializer


class ResourceSearchByChapterAndTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chapter_name = request.query_params.get("chapter")
        resource_type = request.query_params.get("type")

        if not chapter_name or not resource_type:
            return Response({"error": "Please provide both 'chapter' and 'type' as query parameters."}, status=400)

        # Find chapters with matching name
        matching_chapters = Chapter.objects.filter(name__icontains=chapter_name)

        # Filter resources by chapter + resource type
        resources = Resource.objects.filter(
            chapter__in=matching_chapters,
            resource_type=resource_type
        )

        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)




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


# 🔍 Module Search View
class ModuleSearchView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSimpleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['speciality', 'level']  # optional filtering
    search_fields = ['name']

# 🔍 Chapter Search View
class ChapterSearchView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSimpleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'module__name']

# 🔍 Resource Search View
class ResourceSearchView(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'resource_type', 'chapter__name']
