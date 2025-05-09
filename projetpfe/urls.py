
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, )
from .views import CourseSearchView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('programs/', include('programs.urls')),
    path('ai/', include('ai.urls')),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/programs/', include('programs.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/ai/', include('ai.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('search/', CourseSearchView.as_view(), name='course-search'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


