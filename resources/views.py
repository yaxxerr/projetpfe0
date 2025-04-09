from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Welcome to Resources-endpoint")
def resource_view(request):
    return HttpResponse("resources-endpoint")

def access_request_view(request):
    return HttpResponse("access-requests-endpoint")