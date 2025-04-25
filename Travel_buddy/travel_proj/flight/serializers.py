from rest_framework import serializers
from .models import Airport, Flight, Seat, SeatClass
from city.serializers import CitySerializer  # Import CitySerializer

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class SeatClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatClass
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    seat_class = SeatClassSerializer()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_available', 'seat_class']

class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer()
    arrival_airport = AirportSerializer()
    departure_city = CitySerializer()  # Use CitySerializer
    arrival_city = CitySerializer()
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'
