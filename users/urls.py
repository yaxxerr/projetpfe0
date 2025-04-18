from django.urls import path
from . import views
from .views import user_list, user_detail, register_user, LoginView, CurrentUserView, UserUpdateView, MyProfileView, StudentSearchView, ProfessorSearchView, UserSearchView, MyModulesView


urlpatterns = [
    path('', views.index, name='users-home'),
    path('users/', views.user_view, name='users-endpoint'),
    path('professors/', views.professor_view, name='professors-endpoint'),
    path('students/', views.student_view, name='students-endpoint'),
    path('all/', user_list, name='user-list'),
    path('<int:pk>/', user_detail, name='user-detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('register/', register_user, name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='me'),  
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('search/students/', StudentSearchView.as_view(), name='student-search'),
    path("search/professors/", ProfessorSearchView.as_view(), name="search-professors"),
    path("search/", UserSearchView.as_view(), name="users-search"),
    path("my-modules/", MyModulesView.as_view(), name="users-modules"),
]

