from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import Resource, AccessRequest
from .serializers import ResourceSerializer, AccessRequestSerializer

# Create your views here.
def index(request):
    return HttpResponse("Welcome to Resources-endpoint")
def resource_view(request):
    return HttpResponse("resources-endpoint")

def access_request_view(request):
    return HttpResponse("access-requests-endpoint")


# GET: list all resources
# POST: create a new resource (owner = request.user)
class ResourceListCreateView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# GET: retrieve a single resource
# PUT/PATCH: update it
# DELETE: delete it
class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# GET: list all access requests
# POST: create a new access request
class AccessRequestListCreateView(generics.ListCreateAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


# GET: get single access request
# PUT/PATCH: update it
# DELETE: delete it
class AccessRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

