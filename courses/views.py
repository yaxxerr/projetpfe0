from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, filters

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Speciality, Level, Module, Chapter
from .serializers import SpecialitySerializer, LevelSerializer,ResourceSerializer, ModuleSerializer, ChapterSerializer, UserSearchSerializer, ModuleSerializer, ChapterSerializer

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .models import Speciality, Level, Module, Chapter
from .serializers import SpecialitySerializer, LevelSerializer,ResourceSerializer, ModuleSerializer, ChapterSerializer, UserSearchSerializer
from django.core.exceptions import PermissionDenied
from rest_framework import generics, permissions
from .models import Resource, AccessRequest
from .serializers import ResourceSerializer, AccessRequestSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Speciality, Level, Module, Chapter, Resource, AccessRequest
from .serializers import (
    SpecialitySerializer,
    LevelSerializer,
    ModuleSerializer,
    ChapterSerializer,
    ResourceSerializer,
    AccessRequestSerializer,
    UserSearchSerializer,
    ModuleSerializer,
    ChapterSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q
from users.serializers import UserBasicSerializer

User = get_user_model()

# 🌐 Public test
def index(request):
    return HttpResponse("Welcome to courses-endpoint")

# 🔹 GET + POST views
class SpecialityListCreateView(generics.ListCreateAPIView):
    serializer_class = SpecialitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Speciality.objects.exclude(name__iexact='teacher')


class LevelListCreateView(generics.ListCreateAPIView):
    serializer_class = LevelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Level.objects.exclude(name__iexact='teacher')
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
    
    def get_serializer_context(self):
        return {"request": self.request}

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from courses.models import Resource
from courses.serializers import ResourceSerializer

class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Resource.objects.all()
        filter_type = self.request.GET.get('filter')

        if filter_type == 'private':
            queryset = queryset.filter(access_type='private')
        elif filter_type == 'public':
            queryset = queryset.filter(access_type='public')
        elif filter_type == 'default':
            queryset = queryset.filter(owner__is_superuser=True)

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_professor():
            raise PermissionDenied("Only professors can create resources.")
        serializer.save(owner=user)


class AccessRequestListCreateView(generics.ListCreateAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [IsAuthenticated]

# 🔍 Module Search View
class ModuleSearchView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['speciality', 'level']
    search_fields = ['name']

# 🔍 Chapter Search View
class ChapterSearchView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'module__name']

# 🔍 Resource Search View
class ResourceSearchView(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'resource_type', 'chapter__name']


class MyResourcesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_professor():
            return Response({"detail": "Not allowed."}, status=403)
        user = request.user
        queryset = Resource.objects.filter(owner=user)  
        resources = Resource.objects.filter(owner=request.user)
        serializer = ResourceSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

class ResourceUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            resource = Resource.objects.get(pk=pk, owner=request.user)
        except Resource.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = ResourceSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    def get(self, request):
        queryset = Resource.objects.filter(owner=request.user)  # ✅ access request properly
        serializer = ResourceSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class ResourceDeleteView(DestroyAPIView):
    queryset = Resource.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
        def get_serializer_context(self):
             return {"request": self.request}

# 🔍 Flexible resource search
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

        serializer = ResourceSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

# ✅ ✅ ✅ ADDED FOR RESOURCE VISIBILITY CONTROL ✅ ✅ ✅

class MyModuleResourcesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chapters = Chapter.objects.filter(module__in=user.modules.all())
        chapter_ids = chapters.values_list('id', flat=True)

        public_resources = Resource.objects.filter(
            chapter__in=chapter_ids,
            access_type='public'
        )

        added = user.added_resources.all()

        approved_private = Resource.objects.filter(
            access_requests__requester=user,
            access_requests__approved=True
        )

        resources = (public_resources | added | approved_private).distinct()
        serializer = ResourceSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)



class RequestResourceAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resource_id):
        user = request.user
        try:
            resource = Resource.objects.get(id=resource_id)
            if resource.access_type != 'private':
                return Response({"detail": "This resource is not private."}, status=400)

            existing = AccessRequest.objects.filter(resource=resource, requester=user).first()
            if existing:
                return Response({"detail": "Request already sent."}, status=400)

            AccessRequest.objects.create(
                resource=resource,
                requester=user,
                message=request.data.get("message", "")
            )
            return Response({"detail": "✅ Access request sent."})
        except Resource.DoesNotExist:
            return Response({"detail": "❌ Resource not found."}, status=404)

class HandleAccessRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        try:
            access_request = AccessRequest.objects.get(id=request_id)
        except AccessRequest.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        if access_request.resource.owner != request.user:
            return Response({"detail": "Not allowed"}, status=403)

        approved = request.data.get("approved")
        if approved is None:
            return Response({"detail": "Missing 'approved' field"}, status=400)

        access_request.approved = approved
        access_request.save()
        return Response({"success": True, "approved": approved})

class ReceivedAccessRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'professor':
            return Response({"detail": "Forbidden"}, status=403)

        requests = AccessRequest.objects.filter(resource__owner=request.user)
        data = [
            {
                "id": r.id,
                "requester": r.requester.username,
                "resource": r.resource.name,
                "approved": r.approved,
                "created_at": r.created_at
            }
            for r in requests
        ]
        return Response(data)


class SentAccessRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = AccessRequest.objects.filter(requester=request.user)
        data = [
            {
                "id": r.id,
                "resource": r.resource.name,
                "approved": r.approved,
                "created_at": r.created_at
            }
            for r in requests
        ]
        return Response(data)

class ProfessorResourcesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, professor_id):
        try:
            professor = User.objects.get(id=professor_id, user_type='professor')
        except User.DoesNotExist:
            return Response({"error": "Professeur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        resources = Resource.objects.filter(owner=professor)
        serializer = ResourceSerializer(resources, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
