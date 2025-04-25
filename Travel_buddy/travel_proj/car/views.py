# c:\Users\Admin\Desktop\Online Booking and Travel\travel_proj\car\views.py
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction # Not strictly needed for current cancel logic, but good practice
from .models import Car, CarBooking # Import models
from .serializers import CarSerializer, CarBookingSerializer # Import serializers

# --- Keep your existing Car views (List, Detail) ---
class CarList(generics.ListAPIView):
    queryset = Car.objects.all() # Consider filtering available=True
    serializer_class = CarSerializer
    # Add filter backend for city, features etc. if needed

class CarDetail(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'slug' # Or 'pk' if you prefer using ID in URL
# --- End Existing Car Views ---


# --- NEW Car Booking Views ---
class CarBookingListCreateView(generics.ListCreateAPIView):
    """
    List all car bookings for the current user, or create a new car booking.
    """
    serializer_class = CarBookingSerializer
    permission_classes = [IsAuthenticated] # Only logged-in users

    def get_queryset(self):
        """
        Return bookings made by the currently authenticated user.
        """
        return CarBooking.objects.filter(passenger=self.request.user).order_by('-booking_date')

    # perform_create is implicitly handled by ListCreateAPIView passing context
    # to the serializer if needed (which our CarBookingSerializer uses for the user)


class CarBookingDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific car booking owned by the current user.
    """
    serializer_class = CarBookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only see their own bookings.
        """
        return CarBooking.objects.filter(passenger=self.request.user)


class CarBookingCancelView(views.APIView):
    """
    Cancel a specific car booking owned by the current user (soft delete).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Handles the cancellation POST request.
        """
        booking = get_object_or_404(CarBooking, pk=pk, passenger=request.user)

        if booking.is_cancelled:
            return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Perform soft delete
            booking.is_cancelled = True
            booking.save()

            # TODO: Add logic here if car availability needs complex updating based on cancellation
            # For now, just mark booking as cancelled.

            serializer = CarBookingSerializer(booking) # Return updated booking data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error for debugging
            print(f"Error cancelling car booking {pk}: {e}")
            return Response({'message': 'An error occurred during cancellation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- End NEW Car Booking Views ---

