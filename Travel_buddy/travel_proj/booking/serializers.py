# c:\Users\Admin\Desktop\Online Booking and Travel\travel_proj\booking\serializers.py
from rest_framework import serializers
from .models import Booking, Seat
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model() # Get your CustomUser model
# --- End Add ---

# It's often helpful to have a serializer for related models if you want nested data
class SeatSerializer(serializers.ModelSerializer):
    seat_class_name = serializers.CharField(source='seat_class.name', read_only=True) # Example nested field

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_available', 'seat_class_name'] # Add fields you want to see


class BookingSerializer(serializers.ModelSerializer):
    # For Creating: Use PrimaryKeyRelatedField, write_only=True
    seats_input = serializers.PrimaryKeyRelatedField(
        queryset=Seat.objects.all(),
        many=True,
        write_only=True,
        source='seats' # Link this input field to the 'seats' model field for writing
    )
    # For Reading: Use a nested serializer or SlugRelatedField to show seat details
    seats_detail = SeatSerializer(many=True, read_only=True, source='seats') # Use the actual 'seats' field for reading

    # Include passenger email for clarity in response (optional)
    passenger_email = serializers.EmailField(source='passenger.email', read_only=True)
     # Use get_full_name (combines first/last). Falls back gracefully if empty.
    passenger_name = serializers.CharField(source='passenger.get_full_name', read_only=True)
    # Add phone number (relies on CustomUser model having this field)
    passenger_phone_number = serializers.CharField(source='passenger.phone_number', read_only=True)
    # Include flight details (optional)
    flight_info = serializers.StringRelatedField(source='flight', read_only=True)


    class Meta:
        model = Booking
        fields = [
            'id',
            'passenger', # Keep this for internal use/validation if needed
            'passenger_name', # Show this in the response
            'passenger_email', # Show this in the response
            'passenger_phone_number', # Show this in the response
            'flight', # Keep for writing
            'flight_info', # Show this in the response
            'seats_input', # Use this field name in POST/PUT requests
            'seats_detail', # This field will appear in GET responses
            'seats_booked', # Add this field if you want it in the API response
            'booking_date',
            'total_price',
            'is_cancelled'
        ]
        read_only_fields = [
            'id',
            'passenger', # Make passenger read-only as it's set from context
            'booking_date',
            'total_price',
            'is_cancelled', # Cancellation is handled by a separate endpoint
            'passenger_name',
            'passenger_email', 
            'passenger_phone_number',
            'flight_info',
            'seats_detail',
            'seats_booked', # Usually calculated, not set directly by user
        ]
        # Ensure 'seats' (the actual model field) is not listed directly if using source trick
        # Make 'flight' writeable for creation
        extra_kwargs = {
            'flight': {'write_only': True} # Make flight write_only if flight_info is used for reading
        }


    @transaction.atomic
    def create(self, validated_data):
        # 'seats' data comes from 'seats_input' because of the 'source' argument
        seat_data = validated_data.pop('seats', [])
        flight = validated_data.get('flight')
        user = self.context['request'].user

        seat_id_list = [seat.id for seat in seat_data] # Simpler list comprehension

        # Validate seat availability and ownership
        if not seat_id_list:
            raise serializers.ValidationError("At least one seat must be selected.")

        # Check seats belong to the correct flight and are available
        seats = Seat.objects.filter(id__in=seat_id_list, flight=flight)
        if len(seats) != len(seat_id_list):
             raise serializers.ValidationError("One or more selected seats do not belong to the specified flight.")

        unavailable_seats = seats.filter(is_available=False)
        if unavailable_seats.exists():
            raise serializers.ValidationError(
                f"The following seats are unavailable: {', '.join(str(seat.seat_number) for seat in unavailable_seats)}"
            )

        # Calculate total price
        total_price = sum(flight.base_price * seat.seat_class.price_multiplier for seat in seats)

        # Create the booking
        booking = Booking.objects.create(
            passenger=user,
            flight=flight,
            total_price=total_price,
            seats_booked=len(seat_id_list) # Set the number of seats booked
            # **validated_data contains other valid fields like 'is_cancelled' if not read_only
        )

        # Assign seats using IDs and mark them as unavailable
        booking.seats.set(seat_id_list)
        Seat.objects.filter(id__in=seat_id_list).update(is_available=False)

        return booking

    # Note: The default 'update' method from RetrieveUpdateAPIView will use this serializer.
    # If you allow updates, ensure the logic here and read_only_fields are appropriate.
    # Updating seats/flight via a simple PUT/PATCH is often complex and might be better
    # handled by cancellation + new booking.
