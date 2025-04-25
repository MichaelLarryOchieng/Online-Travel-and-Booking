from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Remove Flight import if not used directly in views
# from .models import Flight
from .models import Booking, Seat # Import Seat if needed for serializer adjustments later
# Import the potentially new serializer
from .serializers import BookingSerializer # Keep this for now, consider adding BookingDetailSerializer later
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# --- BookingList View (No changes needed for basic listing) ---
class BookingList(generics.ListCreateAPIView):
    """
    List all bookings for the current user, or create a new booking.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated] # Ensures only logged-in users can access

    def get_queryset(self):
        """
        This view should return a list of all the bookings
        for the currently authenticated user.
        """
        return Booking.objects.filter(passenger=self.request.user).order_by('-booking_date') # Added ordering

    def perform_create(self, serializer):
        """
        Associate the booking with the logged-in user.
        The passenger is set in the serializer's create method using context.
        """
        serializer.save() # Passenger is handled within serializer create method

    # Overriding create just to pass context, which is default behaviour in perform_create
    # Keep your existing create method if you have specific logic, otherwise perform_create is cleaner
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(
    #         data=request.data,
    #         context={'request': request}
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     # Use perform_create for saving, which automatically handles context passing if needed by serializer
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# --- BookingDetail View (Retrieve and potentially Update) ---
class BookingDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a specific booking instance owned by the current user.
    Note: Updating might be limited by serializer's read_only_fields.
    """
    serializer_class = BookingSerializer # Consider using a BookingDetailSerializer here (see Step 2)
    permission_classes = [IsAuthenticated] # Ensures only logged-in users can access

    def get_queryset(self):
        """
        This view should return a specific booking owned by the
        currently authenticated user.
        """
        return Booking.objects.filter(passenger=self.request.user)

    # The default RetrieveUpdateAPIView handles GET (retrieve) and PUT/PATCH (update)
    # using the queryset defined above, so explicit get/update methods are often not needed
    # unless you have custom logic. The get_queryset ensures ownership.

    # Example: If you wanted custom update logic (though often not needed here)
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object() # get_object uses get_queryset, ensuring ownership
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


# --- BookingCancel View ---
class BookingCancelView(APIView):
    """
    Cancel a specific booking owned by the current user.
    """
    permission_classes = [IsAuthenticated] # Ensures only logged-in users can access

    def post(self, request, pk):
        """
        Handles the cancellation POST request.
        """
        # Get the booking, ensuring it belongs to the current user
        booking = get_object_or_404(Booking, pk=pk, passenger=request.user)

        if booking.is_cancelled:
            return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                booking.is_cancelled = True
                booking.save()

                # Make the seats available again
                booking.seats.all().update(is_available=True) # More efficient update

            # Use the same serializer used for detail view for consistency
            serializer = BookingSerializer(booking) # Consider BookingDetailSerializer if created
            return Response(serializer.data, status=status.HTTP_200_OK)
        # DoesNotExist is handled by get_object_or_404 now
        except Exception as e:
            # Log the exception e for debugging
            print(f"Error cancelling booking {pk}: {e}")
            return Response({'message': 'An error occurred during cancellation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) # Use 500 for unexpected errors


