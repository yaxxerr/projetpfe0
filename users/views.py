from django.shortcuts import render
from .models import User, Follow
from .serializers import (
    StudentSerializer,
    AssignModulesSerializer,
    FollowSerializer,
    UserBasicSerializer,
    UserSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
    FollowingSerializer
)
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from courses.models import Module
from courses.serializers import ModuleSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import Module, Chapter, Resource
from courses.serializers import ModuleSerializer

class MyModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        modules = user.modules.prefetch_related('chapters__resources').all()

        data = []

        for module in modules:
            module_data = {
                "id": module.id,
                "name": module.name,
                "description": module.description,
                "chapters": []
            }

            for chapter in module.chapters.all():
                all_resources = chapter.resources.all()
                default_resources = all_resources.filter(owner__is_superuser=True)
                private_resources = all_resources.filter(access_type="private")

                chapter_data = {
                    "id": chapter.id,
                    "name": chapter.name,
                    "resources": {
                        "all": [
                            {
                                "id": r.id,
                                "name": r.name,
                                "resource_type": r.resource_type,
                                "access_type": r.access_type,
                                "link": r.link,
                            } for r in all_resources
                        ],
                        "default": [
                            {
                                "id": r.id,
                                "name": r.name,
                                "resource_type": r.resource_type,
                                "access_type": r.access_type,
                                "link": r.link,
                            } for r in default_resources
                        ],
                        "private": [
                            {
                                "id": r.id,
                                "name": r.name,
                                "resource_type": r.resource_type,
                                "access_type": r.access_type,
                                "link": r.link,
                            } for r in private_resources
                        ]
                    }
                }

                module_data["chapters"].append(chapter_data)

            data.append(module_data)

        return Response(data)


# ✅ REGISTER (version de ton ami)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ ASSIGN MODULES
class AssignModulesView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignModulesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.level = serializer.validated_data['level']
            user.speciality = serializer.validated_data['speciality']
            user.save()
            user.assign_modules_to_student()
            return Response({'success': 'Modules assigned successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Simple messages
def index(request): return HttpResponse("Welcome to users-endpoint")
def user_view(request): return HttpResponse("users-endpoint")
def professor_view(request): return HttpResponse("professors-endpoint")
def student_view(request): return HttpResponse("students-endpoint")


# GET user list
User = get_user_model()

@api_view(['GET'])
def user_list(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# LOGIN
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("✅ Data received from frontend:")
        print(request.data)
        return super().post(request, *args, **kwargs)


# /me/
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# /<id>/update/
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# /my-profile/
class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# /me/edit/
class UpdateMyProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# /search/students/
class StudentSearchView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(
            user_type='student'
        ).filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )


# /search/professors/
class ProfessorSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "")
        professors = User.objects.filter(user_type='professor', username__icontains=query)
        return Response(UserBasicSerializer(professors, many=True).data)


# /search/
class UserSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=query)
        data = [
            {
                "id": user.id,
                "username": user.username,
                "user_type": user.user_type,
                "email": user.email,
            }
            for user in users
        ]
        return Response(data)




# /follow/
class FollowProfessorView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class MyFollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_professor():
            return Response({"detail": "Not allowed."}, status=403)

        followers = request.user.followers.select_related('student')
        data = [{"id": f.student.id, "username": f.student.username} for f in followers]
        return Response(data)

class MyFollowingsView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(student=self.request.user)

class UnfollowProfessorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = request.user
        professor_username = request.data.get("professor_username")

        if not professor_username:
            return Response({"detail": "Professor username is required."}, status=400)

        try:
            professor = User.objects.get(username=professor_username, user_type='professor')
        except User.DoesNotExist:
            return Response({"detail": "Professor not found."}, status=404)

        try:
            follow = Follow.objects.get(student=student, professor=professor)
            follow.delete()
            return Response({"detail": f"Unfollowed {professor.username} successfully."})
        except Follow.DoesNotExist:
            return Response({"detail": "You are not following this professor."}, status=400)



# /modules/<id>/
class ModuleDetailView(RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [AllowAny]
class UpdateMyProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # ✅ Très important !


