# c:\Users\Admin\Desktop\Online Booking and Travel\travel_proj\car\urls.py
from django.urls import path
# Import all the necessary views from car.views
from .views import (
    CarList,
    CarDetail,
    CarBookingListCreateView,
    CarBookingDetailView,
    CarBookingCancelView
)

urlpatterns = [
    # URLs for viewing Cars
    path('cars/', CarList.as_view(), name='car-list'), # Changed view name to CarList
    # Use slug or pk consistently with your CarDetail view's lookup_field
    path('cars/<slug:slug>/', CarDetail.as_view(), name='car-detail'), # Assuming CarDetail uses slug
    # path('cars/<int:pk>/', CarDetail.as_view(), name='car-detail'), # Alternative if using pk

    # URLs for Car Bookings
    path('car-bookings/', CarBookingListCreateView.as_view(), name='carbooking-list-create'),
    path('car-bookings/<int:pk>/', CarBookingDetailView.as_view(), name='carbooking-detail'),
    path('car-bookings/<int:pk>/cancel/', CarBookingCancelView.as_view(), name='carbooking-cancel'),
]
