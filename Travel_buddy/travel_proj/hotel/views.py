from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel  # Import your Hotel model
from .serializers import HotelSerializer  # Import your Hotel serializer

class HotelListView(APIView):
    """
    View to list all hotels, or create a new hotel.
    """
    def get(self, request, format=None):
        """
        Returns a list of all hotels.
        """
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Creates a new hotel.
        """
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HotelDetailView(APIView):
    """
    View to retrieve, update, or delete a hotel instance.
    """
    def get_object(self, pk):
        """
        Helper method to get a hotel instance by primary key.
        """
        try:
            return Hotel.objects.get(pk=pk)
        except Hotel.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        """
        Retrieves a hotel instance.
        """
        hotel = self.get_object(pk)
        if not hotel:
            return Response({"message": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Updates a hotel instance.
        """
        hotel = self.get_object(pk)
        if not hotel:
            return Response({"message": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Partially updates a hotel instance.
        """
        hotel = self.get_object(pk)
        if not hotel:
            return Response({"message": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes a hotel instance.
        """
        hotel = self.get_object(pk)
        if not hotel:
            return Response({"message": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


