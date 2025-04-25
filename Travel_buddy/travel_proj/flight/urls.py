from django.urls import path
from flight.views import FlightList, FlightDetail, AirportList, AirportDetail, SeatList, SeatDetail, SeatClassList, SeatClassDetail

urlpatterns = [
    path('flights/', FlightList.as_view()),
    path('flights/<int:pk>/', FlightDetail.as_view()),
    path('airports/', AirportList.as_view()),
    path('airports/<int:pk>/', AirportDetail.as_view()),
    path('seats/', SeatList.as_view()),
    path('seats/<int:pk>/', SeatDetail.as_view()),
    path('seatclasses/', SeatClassList.as_view()),  # Add this line
    path('seatclasses/<int:pk>/', SeatClassDetail.as_view()), # Optional: for individual seat class details
]