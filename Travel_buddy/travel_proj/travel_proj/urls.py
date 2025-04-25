"""
URL configuration for travel_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/travel_buddy/', include('djoser.urls')),
    path('api/travel_buddy/', include('djoser.urls.authtoken')),
    path('api/travel_buddy/', include('city.urls')),  # Include the city app URLs
    path('api/travel_buddy/', include('attractions.urls')),  # Include the attractions app URLs
    path('api/travel_buddy/', include('flight.urls')),  # Include the flight app URLs
    path('api/travel_buddy/', include('car.urls')),  # Include the car_rentals app URLs
    path('api/travel_buddy/', include('terrain_condition.urls')),  # Include the terrain_condition app URLs
    path('api/travel_buddy/', include('booking.urls')),  # Include the booking app URLs
    path('api/travel_buddy/', include('hotel.urls')),  # Include the hotel app URLs
    path('api/travel_buddy/accounts/', include('accounts.urls')),  # Include the accounts app URLs
    path('api/travel_buddy/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add token refresh endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)