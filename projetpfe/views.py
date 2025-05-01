# projetpfe/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from courses.models import Speciality, Module, Chapter, Resource, Level
from users.models import User
from courses.serializers import SpecialitySerializer, LevelSerializer, ModuleSerializer, ChapterSerializer, ResourceSerializer
from users.serializers import  UserBasicSerializer

class CourseSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')

        # Search all models
        specialities = Speciality.objects.filter(name__icontains=query)
        levels = Level.objects.filter(name__icontains=query)
        modules = Module.objects.filter(name__icontains=query)
        chapters = Chapter.objects.filter(name__icontains=query)
        resources = Resource.objects.filter(name__icontains=query)
        users = User.objects.filter(username__icontains=query)

        return Response({
            "specialities": SpecialitySerializer(specialities, many=True).data,
            "levels": LevelSerializer(levels, many=True).data,
            "modules": ModuleSimpleSerializer(modules, many=True).data,
            "chapters": ChapterSimpleSerializer(chapters, many=True).data,
            "resources": ResourceSerializer(resources, many=True).data,
            "users": UserBasicSerializer(users, many=True).data,
        })