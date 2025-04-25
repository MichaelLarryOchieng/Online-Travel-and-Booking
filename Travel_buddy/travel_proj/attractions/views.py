from django.shortcuts import render
from .serializers import AttractionSerializer
from rest_framework.views import APIView #APIView is a fundamental class provided by the Django REST framework.
#It provides a lot of the boilerplate code and functionality needed to handle HTTP requests (GET, POST, PUT, DELETE, etc.) in a RESTful way.
from .models import Attraction
from rest_framework.response import Response

class AttractionListView(APIView):
    def get(self, request):
        attractions = Attraction.objects.all()[0:10]  # Limit to first 10 attractions using [0:10] slicing
        serializer = AttractionSerializer(attractions, many=True)  # many=True indicates that we are serializing a list of objects/many objects
        return Response(serializer.data)

# Create your views here.
