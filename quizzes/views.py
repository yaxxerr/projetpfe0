from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Welcome to quizzes-endpoint")

def quiz_view(request):
    return HttpResponse("quizzes-endpoint")

def question_view(request):
    return HttpResponse("questions-endpoint")

def answer_view(request):
    return HttpResponse("answers-endpoint")
