from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Welcome to users-endpoint")
def user_view(request):
    return HttpResponse("users-endpoint")

def professor_view(request):
    return HttpResponse("professors-endpoint")

def student_view(request):
    return HttpResponse("students-endpoint")