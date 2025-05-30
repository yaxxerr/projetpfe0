from django.urls import path
from . import views
from .views import LevelsBySpecialityView, SpecialityListCreateView, LevelListCreateView, ModuleListCreateView, ChapterListCreateView, ModuleSearchView, ChapterSearchView, ResourceSearchView
from django.urls import path
from .views import ResourceListCreateView,MyResourcesView,ResourceDeleteView,ResourceUpdateView, AccessRequestListCreateView,ResourceSearchFlexibleView, ProfessorResourcesView
from .views import ModuleDetailView

from .views import (
    SpecialityListCreateView,
    LevelListCreateView,
    ModuleListCreateView,
    ChapterListCreateView,
    ModuleSearchView,
    ChapterSearchView,
    ResourceSearchView,
    ResourceListCreateView,
    AccessRequestListCreateView,
    ResourceSearchFlexibleView,
    ModuleDetailView,
    MyModuleResourcesView,
    HandleAccessRequestView,
    RequestResourceAccessView
)
urlpatterns = [
    path('', views.index, name='courses-home'),
    path('specialities/', SpecialityListCreateView.as_view(), name='speciality-endpoint'),
    path('levels/', LevelListCreateView.as_view(), name='level-list-create'),
    path('modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
    path('chapters/', ChapterListCreateView.as_view(), name='chapter-list-create'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/access-requests/', AccessRequestListCreateView.as_view(), name='access-request-list-create'),
    path('resources/search/', ResourceSearchFlexibleView.as_view(), name='flexible-resource-search'),
    path('resources/my/', MyResourcesView.as_view(), name='my-resources'),
    path('resources/<int:pk>/edit/', ResourceUpdateView.as_view(), name='edit-resource'),
    path('resources/<int:pk>/delete/', ResourceDeleteView.as_view(), name='delete-resource'),
    path('<int:professor_id>/resources/', ProfessorResourcesView.as_view(), name='professor-resources'),
    path('speciality/<int:speciality_id>/levels/', LevelsBySpecialityView.as_view(), name='levels-by-speciality'),

# 🔍 Search endpoints
    path('search/modules/', ModuleSearchView.as_view(), name='search-modules'),
    path('search/chapters/', ChapterSearchView.as_view(), name='search-chapters'),
    path('search/resources/', ResourceSearchView.as_view(), name='search-resources'),
    path('resources/search/', ResourceSearchFlexibleView.as_view(), name='flexible-resource-search'),

    # ✅ New resource control endpoints
    path('resources/request/<int:resource_id>/', RequestResourceAccessView.as_view(), name='request-resource-access'),
    path('resources/access-requests/received/', views.ReceivedAccessRequestsView.as_view(), name='received-access-requests'),
    path('resources/access-requests/sent/', views.SentAccessRequestsView.as_view(), name='sent-access-requests'),
    path('resources/handle-request/<int:request_id>/', HandleAccessRequestView.as_view(), name='handle-access-request')
    
]
