# c:\Users\Admin\Desktop\Online Booking and Travel\travel_proj\car\serializers.py
from rest_framework import serializers
from .models import Car, CarBooking # Import both models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Import CitySerializer if needed for nested Car representation
from city.serializers import CitySerializer # Assuming you have this

User = get_user_model()

# --- Serializer for nested Car display in Booking ---
class SimpleCarSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for displaying basic car info within a booking.
    """
    city_name = serializers.CharField(source='city.name', read_only=True)
    thumbnail = serializers.CharField(source='get_thumbnail', read_only=True)

    class Meta:
        model = Car
        # Include fields you want to see when viewing a car booking
        fields = ('id', 'name', 'company', 'model', 'city_name', 'price_per_day', 'thumbnail')

# --- Serializer for Car Booking ---
class CarBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and viewing CarBooking instances.
    """
    # For reading: Use the nested serializer for car details
    car_details = SimpleCarSerializer(source='car', read_only=True)
    # For writing: Expect the car ID
    car = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), # Consider filtering available cars later
        write_only=True
    )
    # For reading: Passenger details
    passenger_name = serializers.CharField(source='passenger.get_full_name', read_only=True)
    passenger_email = serializers.EmailField(source='passenger.email', read_only=True)
    passenger_phone_number = serializers.CharField(source='passenger.phone_number', read_only=True)

    # Input fields for creation (ensure frontend sends datetime format)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    class Meta:
        model = CarBooking
        fields = [
            'id',
            'passenger', # Internal reference, set from context
            'passenger_name', # Read-only passenger detail
            'passenger_email', # Read-only passenger detail
            'passenger_phone_number', # Read-only passenger detail
            'car', # Write-only ID input
            'car_details', # Read-only nested object output
            'start_date', # Input and Output
            'end_date', # Input and Output
            'total_price', # Read-only, calculated
            'booking_date', # Read-only, auto-set
            'is_cancelled', # Read-only, set via cancel view
        ]
        read_only_fields = [
            'id', 'passenger', 'total_price', 'booking_date', 'is_cancelled',
            'passenger_name', 'passenger_email', 'passenger_phone_number', 'car_details',
        ]

    def validate(self, data):
        """
        Custom validation for dates and potentially availability.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        car = data.get('car')

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({"end_date": "End date must be after start date."})
            # Use date part for past check if time isn't critical for booking start
            if start_date.date() < timezone.now().date():
                 raise serializers.ValidationError({"start_date": "Start date cannot be in the past."})

        # TODO: Add robust availability check for the date range
        # This requires querying existing CarBooking records for overlaps
        # existing_bookings = CarBooking.objects.filter(
        #     car=car,
        #     is_cancelled=False,
        #     start_date__lt=end_date, # Booking starts before requested end
        #     end_date__gt=start_date  # Booking ends after requested start
        # ).exists()
        # if existing_bookings:
        #     raise serializers.ValidationError({"car": f"Car '{car.name}' is already booked during the selected dates."})

        return data

    def create(self, validated_data):
        """
        Calculate total price and create the booking, associating the user.
        """
        car = validated_data.get('car')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        # Get user from context passed by the view (ensure view passes context)
        user = self.context['request'].user

        # Calculate duration using the model method
        # Create a temporary instance just for calculation if needed, or calculate directly
        temp_booking = CarBooking(start_date=start_date, end_date=end_date)
        days = temp_booking.calculate_duration_days()

        # Calculate total price
        total_price = days * car.price_per_day

        # Create the booking instance, including the user
        car_booking = CarBooking.objects.create(
            passenger=user,
            total_price=total_price,
            **validated_data # Pass car, start_date, end_date from validated data
        )
        return car_booking

# --- Serializer for Listing/Detail view of Cars ---
class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for listing cars and showing car details.
    """
    city_name = serializers.CharField(source='city.name', read_only=True)
    # Explicitly declare fields using methods as source
    thumbnail = serializers.CharField(source='get_thumbnail', read_only=True)
    image_url = serializers.CharField(source='get_image', read_only=True) # Use get_image method

    # Optional: Include full city details if needed for car list/detail
    # city = CitySerializer(read_only=True)

    class Meta:
        model = Car
        # List all fields from the model and the explicitly declared ones
        fields = (
            "id", "name", "slug", "company", "model", "year", "color", "seats",
            "luggage_capacity", "fuel_type", "transmission", "air_conditioning",
            "gps", "bluetooth", "child_seat", "cruise_control", "parking_sensors",
            "heated_seats", "sunroof", "navigation_system", "price_per_day",
            "availability", "description",
            # Use the declared field names:
            "image_url", # Corresponds to source='get_image'
            "thumbnail", # Corresponds to source='get_thumbnail'
            "city", # Foreign key ID (useful if you need to filter by city ID)
            "city_name" # Declared field using source='city.name'
            # Add 'city' here instead of 'city_name' if using the nested CitySerializer above
        )
        # read_only_fields are less critical here as fields are declared read_only above
        # but can be listed for clarity if desired.
        # read_only_fields = ("image_url", "thumbnail", "city_name")



