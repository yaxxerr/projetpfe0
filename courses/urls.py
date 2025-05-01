from django.urls import path
from . import views
from .views import SpecialityListCreateView, LevelListCreateView, ModuleListCreateView, ChapterListCreateView, ModuleSearchView, ChapterSearchView, ResourceSearchView
from django.urls import path
from .views import ResourceListCreateView,MyResourcesView,ResourceDeleteView,ResourceUpdateView, AccessRequestListCreateView,ResourceSearchFlexibleView
from .views import ModuleDetailView


urlpatterns = [
    path('', views.index, name='courses-home'),
    path('specialities/', SpecialityListCreateView.as_view(), name='speciality-endpoint'),
    path('levels/', LevelListCreateView.as_view(), name='level-list-create'),
    path('modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('chapters/', ChapterListCreateView.as_view(), name='chapter-list-create'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/access-requests/', AccessRequestListCreateView.as_view(), name='access-request-list-create'),
    path('resources/search/', ResourceSearchFlexibleView.as_view(), name='flexible-resource-search'),
    path('resources/my/', MyResourcesView.as_view(), name='my-resources'),
    path('resources/<int:pk>/edit/', ResourceUpdateView.as_view(), name='edit-resource'),
    path('resources/<int:pk>/delete/', ResourceDeleteView.as_view(), name='delete-resource'),
    path('search/modules/', ModuleSearchView.as_view(), name='search-modules'),
    path('search/chapters/', ChapterSearchView.as_view(), name='search-chapters'),
    path('search/resources/', ResourceSearchView.as_view(), name='search-resources'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
]