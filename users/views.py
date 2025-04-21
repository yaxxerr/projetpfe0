from django.shortcuts import render
from .models import User, Follow
from .serializers import StudentSerializer,AssignModulesSerializer,FollowSerializer, UserBasicSerializer,UserSerializer, RegisterSerializer, UserUpdateSerializer
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from courses.serializers import ModuleSerializer


from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import AssignModulesSerializer

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


#simple message
def index(request):
    return HttpResponse("Welcome to users-endpoint")
def user_view(request):
    return HttpResponse("users-endpoint")

def professor_view(request):
    return HttpResponse("professors-endpoint")

def student_view(request):
    return HttpResponse("students-endpoint")

#get apis
User = get_user_model()

@api_view(['GET'])
def user_list(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("❌ Error in user_list view:", str(e))
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)


#post apis
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /login/
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    authentication_classes=[]
    serializer_class = TokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        print("✅ Data received from frontend:")
        print(request.data)  # This will print {"username": "...", "password": "..."}

        # Optional: You can also log headers or other meta data
        # print(request.headers)

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


class ProfessorSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("q", "")
        professors = User.objects.filter(user_type='professor', username__icontains=query)
        return Response(UserBasicSerializer(professors, many=True).data)



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


class MyModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        modules = user.modules.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)



class UpdateMyProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowProfessorView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

