from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import get_user_model


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
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)