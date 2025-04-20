from django.urls import path
from . import views
from .views import SpecialityListCreateView, LevelListCreateView, ModuleListCreateView, ChapterListCreateView, ModuleSearchView, ChapterSearchView, ResourceSearchView
from django.urls import path
from .views import ResourceListCreateView, AccessRequestListCreateView,ResourceSearchFlexibleView


urlpatterns = [
    path('', views.index, name='courses-home'),
    path('specialities/', SpecialityListCreateView.as_view(), name='speciality-endpoint'),
    path('levels/', LevelListCreateView.as_view(), name='level-list-create'),
    path('modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('chapters/', ChapterListCreateView.as_view(), name='chapter-list-create'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/access-requests/', AccessRequestListCreateView.as_view(), name='access-request-list-create'),
    path('search/modules/', ModuleSearchView.as_view(), name='search-modules'),
    path('search/chapters/', ChapterSearchView.as_view(), name='search-chapters'),
    path('resources/search/', ResourceSearchFlexibleView.as_view(), name='flexible-resource-search'),
    path('search/resources/', ResourceSearchView.as_view(), name='search-resources'),
]