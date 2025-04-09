from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to courses-endpoint")
def speciality_view(request):
    return HttpResponse("speciality-endpoint")

def level_view(request):
    return HttpResponse("level-endpoint")

def module_view(request):
    return HttpResponse("module-endpoint")

def chapter_view(request):
    return HttpResponse("chapter-endpoint")
