# projetpfe/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from courses.models import Speciality, Module, Chapter, Resource, Level
from users.models import User
from courses.serializers import (
    SpecialitySerializer,
    LevelSerializer,
    ModuleSerializer,
    ChapterSerializer,
    ResourceSerializer
)
from users.serializers import UserBasicSerializer

class CourseSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({"error": "Empty search query."}, status=400)

        # Filter each model with intelligent Q filtering
        specialities = Speciality.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        levels = Level.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        modules = Module.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        chapters = Chapter.objects.filter(name__icontains=query)
        resources = Resource.objects.filter(name__icontains=query)
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))

        # Use context-aware serializers
        context = {'request': request}
        return Response({
            "specialities": SpecialitySerializer(specialities, many=True, context=context).data,
            "levels": LevelSerializer(levels, many=True, context=context).data,
            "modules": ModuleSerializer(modules, many=True, context=context).data,
            "chapters": ChapterSerializer(chapters, many=True, context=context).data,
            "resources": ResourceSerializer(resources, many=True, context=context).data,
            "users": UserBasicSerializer(users, many=True, context=context).data,
        })
