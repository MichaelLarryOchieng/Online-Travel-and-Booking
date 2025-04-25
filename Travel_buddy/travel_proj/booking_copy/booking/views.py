from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Flight
from .serializers import BookingSerializer
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class BookingList(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(passenger=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}  #  Corrected context.  Do NOT pass flight here.
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookingDetail(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def update(self, request, pk=None, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = self.get_serializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class BookingCancelView(APIView):
    def post(self, request, pk):
        try:
            booking = get_object_or_404(Booking, pk=pk)
            if booking.is_cancelled:
                return Response({'message': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                booking.is_cancelled = True
                booking.save()

                for seat in booking.seats.all():
                    seat.is_available = True
                    seat.save()
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
