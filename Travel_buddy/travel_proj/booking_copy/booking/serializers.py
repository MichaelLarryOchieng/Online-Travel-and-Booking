from rest_framework import serializers
from .models import Booking, Seat
from django.db import transaction

class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'flight', 'seats', 'booking_date', 'total_price', 'is_cancelled']
        read_only_fields = ['id', 'booking_date', 'total_price', 'passenger']
    
    @transaction.atomic
    def create(self, validated_data):
        # Extract and process seat data safely
        seat_data = validated_data.pop('seats', [])
        flight = validated_data.get('flight')
        user = self.context['request'].user
        
        # Convert to IDs if we received objects
        seat_id_list = []
        for seat in seat_data:
            if isinstance(seat, int):
                seat_id_list.append(seat)
            else:
                seat_id_list.append(seat.id)
        
        # Validate seat availability and ownership
        if not seat_id_list:
            raise serializers.ValidationError("At least one seat must be selected.")
            
        seats = Seat.objects.filter(id__in=seat_id_list, flight=flight, is_available=True)
        if len(seats) != len(seat_id_list):
            unavailable_seats = Seat.objects.filter(id__in=seat_id_list, is_available=False)
            raise serializers.ValidationError(
                f"The following seats are unavailable: {', '.join(str(seat.seat_number) for seat in unavailable_seats)}"
            )
        
        # Calculate total price
        total_price = sum(flight.base_price * seat.seat_class.price_multiplier for seat in seats)
        
        # Create the booking including the seats_booked field
        booking = Booking.objects.create(
            passenger=user,
            flight=flight,
            total_price=total_price,
            seats_booked=len(seat_id_list)  # Set the number of seats booked
        )
        
        # Assign seats using IDs and mark them as unavailable
        booking.seats.set(seat_id_list)  # Use IDs instead of objects
        Seat.objects.filter(id__in=seat_id_list).update(is_available=False)
        
        return booking