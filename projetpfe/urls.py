
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    path('resources/', include('resources.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('programs/', include('programs.urls')),
    path('ai/', include('ai.urls')),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls')),
]

