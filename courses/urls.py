from django.urls import path
from . import views
from .views import SpecialityListCreateView, LevelListCreateView, ModuleListCreateView, ChapterListCreateView
from django.urls import path
from .views import ResourceListCreateView, AccessRequestListCreateView

urlpatterns = [
    path('', views.index, name='courses-home'),
    path('specialities/', SpecialityListCreateView.as_view(), name='speciality-endpoint'),
    path('levels/', LevelListCreateView.as_view(), name='level-list-create'),
    path('modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('chapters/', ChapterListCreateView.as_view(), name='chapter-list-create'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
    path('resources/access-requests/', AccessRequestListCreateView.as_view(), name='access-request-list-create'),
]