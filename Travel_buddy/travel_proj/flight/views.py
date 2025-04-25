from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Flight, Airport, Seat, SeatClass
from .serializers import FlightSerializer, AirportSerializer, SeatSerializer, SeatClassSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.utils import timezone



class FlightList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['departure_city', 'arrival_city', 'departure_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        date_param = self.request.query_params.get('date')
        if date_param:
            try:
                filter_date = timezone.datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(departure_time__date=filter_date)
            except ValueError:
                pass  # Invalid date format, ignore the filter
        return queryset

class FlightDetail(APIView):
    """
    View to display the details of a specific flight, including available seats with their classes and prices.
    """
    def get(self, request, pk):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightSerializer(flight)
        return Response(serializer.data)

class AirportList(generics.ListAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class AirportDetail(generics.RetrieveAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class SeatList(generics.ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatDetail(generics.RetrieveAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class SeatClassList(generics.ListAPIView):
    queryset = SeatClass.objects.all()
    serializer_class = SeatClassSerializer

class SeatClassDetail(generics.RetrieveAPIView):
    queryset = SeatClass.objects.all()
    serializer_class = SeatClassSerializer
