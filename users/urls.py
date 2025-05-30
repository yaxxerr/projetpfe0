from django.urls import path
from .views import professor_view, ProfessorListView, ProfessorModulesView
from . import views
from .views import (
    user_list,
    user_detail,
    FollowProfessorView,
    RegisterView,  # ✅ Ton ami utilise cette vue
    AssignModulesView,
    LoginView,
    CurrentUserView,
    UserUpdateView,
    MyProfileView,
    StudentSearchView,
    ProfessorSearchView,
    UserSearchView,
    MyModulesView,
    UpdateMyProfileView,
    ModuleDetailView,
    MyFollowersView,
    MyFollowingsView,
    UserProfileView,
    UnfollowProfessorView,
    ProfessorListView
)

urlpatterns = [

    path('all/', user_list, name='user-list'),
    path('<int:pk>/', user_detail, name='user-detail'),
    path('professors/', ProfessorListView.as_view(), name='professor-list'),
    path('professor/', professor_view, name='professor-info'),  
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='login'),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path('me/', CurrentUserView.as_view(), name='me'),  
    path('me/edit/', UpdateMyProfileView.as_view(), name='update-my-profile'),
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('search/students/', StudentSearchView.as_view(), name='student-search'),
    path('search/professors/', ProfessorSearchView.as_view(), name='search-professors'),
    path('search/', UserSearchView.as_view(), name='users-search'),
    path('my-modules/', MyModulesView.as_view(), name='users-modules'),
    path('assign-my-modules/', AssignModulesView.as_view(), name='assign-my-modules'),
    path('choosemodules/', ProfessorModulesView.as_view(), name='professor-modules'),
    path('follow/', FollowProfessorView.as_view(), name='follow-professor'),
    path('my-followers/', MyFollowersView.as_view(), name='my-followers'),
    path('my-followings/', MyFollowingsView.as_view(), name='my-followings'),
    path('unfollow/', UnfollowProfessorView.as_view(), name='unfollow-professor'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
   
]
