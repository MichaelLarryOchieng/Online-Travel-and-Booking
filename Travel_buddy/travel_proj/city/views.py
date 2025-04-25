from django.shortcuts import render
from .serializers import CitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import City

class CityListView(APIView):
    def get(self, request):
        cities = City.objects.all()[0:10] # Limit to first 10 cities using [0:10] slicing
        serializer = CitySerializer(cities, many=True)# many=True indicates that we are serializing a list of objects/many objects
        return Response(serializer.data)
    
# Create your views here.
