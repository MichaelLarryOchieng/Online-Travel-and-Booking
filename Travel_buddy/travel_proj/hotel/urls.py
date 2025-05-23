from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),
]
