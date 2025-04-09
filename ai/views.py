from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Ai-endpoint")
def chatbot_messages_view(request):
    return HttpResponse("chatbot-messages-endpoint")

def generated_quizzes_view(request):
    return HttpResponse("generated-quizzes-endpoint")

def program_recommendations_view(request):
    return HttpResponse("program-recommendations-endpoint")

def performance_tracking_view(request):
    return HttpResponse("performance-tracking-endpoint")