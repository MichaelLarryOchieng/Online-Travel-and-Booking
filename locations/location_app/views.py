from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Locations
from .serializers import LocationsSerializer

class LocationsList(generics.ListAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

def locations_html(request):
    return render(request, 'locations/locations.html')

def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")
# Create your views here.
