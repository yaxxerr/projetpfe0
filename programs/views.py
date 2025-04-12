from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import Program
from .serializers import ProgramSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

def index(request):
    return HttpResponse("Welcome to programs-endpoint")
def program_view(request):
    return HttpResponse("programs-endpoint")

    # programs/views.py

#GET POST
class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

#GET
class MyProgramsListView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Program.objects.filter(student=self.request.user)
