from django.shortcuts import get_object_or_404, render
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
from django.db.models import Q, Prefetch
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from courses.models import AccessRequest
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from courses.models import Module
from courses.serializers import ModuleSerializer, ResourceSerializer
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from courses.models import Module, Chapter, Resource
from courses.serializers import ModuleSerializer
from courses.models import Level, Speciality



class MyModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        filter_type = request.query_params.get("filter")  # 'all', 'default', 'private'
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

                if filter_type == "default":
                    resources = all_resources.filter(owner__is_superuser=True)

                elif filter_type == "private":
                    approved_ids = AccessRequest.objects.filter(
                        requester=user,
                        approved=True
                    ).values_list("resource_id", flat=True)

                    resources = all_resources.filter(
                        access_type="private",
                        id__in=approved_ids
                    )

                else:  # default to "all"
                    resources = all_resources

                chapter_data = {
                    "id": chapter.id,
                    "name": chapter.name,
                    "resources": ResourceSerializer(resources, many=True, context={"request": request}).data
                }

                module_data["chapters"].append(chapter_data)

            data.append(module_data)

        return Response(data)

# ✅ REGISTER (version de ton ami)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user.user_type == "professor":
            # 🔧 Auto-assign "teacher" level and speciality if professor
            try:
                teacher_level = Level.objects.get(name__iexact="teacher")
                teacher_spec = Speciality.objects.get(name__iexact="teacher")
                user.level = teacher_level
                user.speciality = teacher_spec
                user.save()
            except (Level.DoesNotExist, Speciality.DoesNotExist):
                return Response({
                    "error": "❌ 'teacher' level or speciality not found in database."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # ✅ For students, assign modules normally
            user.assign_modules_to_student()

        return Response({
            "message": "✅ Inscription réussie",
            "username": user.username,
            "user_type": user.user_type
        }, status=status.HTTP_201_CREATED)

        
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


class ProfessorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        professors = User.objects.filter(user_type='professor')
        serializer = UserSerializer(professors, many=True, context={'request': request})
        return Response(serializer.data)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, context={"request": request})
        is_following = user in request.user.following.all() if request.user != user else False

        return Response({
            "user": serializer.data,
            "is_following": is_following
        })

# ✅ Endpoint pour obtenir les infos du professeur connecté
# ✅ Endpoint pour obtenir les infos du professeur connecté
# ✅ Endpoint pour obtenir les infos du professeur connecté
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def professor_view(request):
    user = request.user
    if user.user_type != 'professor':
        return Response({'error': 'Access denied'}, status=403)

    return JsonResponse({
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "user_type": user.user_type,
        "profile_photo": user.profile_photo.url if user.profile_photo else None
    })

class ProfessorModulesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_professor():
            return Response({"detail": "Only professors can view assigned modules."}, status=status.HTTP_403_FORBIDDEN)

        modules = user.modules.all().order_by("name")

        resource_qs = Resource.objects.filter(owner=user)
        chapters_qs = Chapter.objects.prefetch_related(
            Prefetch("resources", queryset=resource_qs)
        )
        modules = modules.prefetch_related(Prefetch("chapters", queryset=chapters_qs))

        serializer = ModuleSerializer(modules, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user.is_professor():
            return Response({"detail": "Only professors can assign modules."},
                            status=status.HTTP_403_FORBIDDEN)

        module_ids = request.data.get("module_ids", [])
        if not isinstance(module_ids, list):
            return Response({"detail": "'module_ids' must be a list."},
                            status=status.HTTP_400_BAD_REQUEST)

        modules = Module.objects.filter(id__in=module_ids)
        user.modules.set(modules)
        user.save()

        return Response({"detail": "✅ Modules assigned successfully."}, status=status.HTTP_200_OK)