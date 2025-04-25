from django.contrib import admin
from .models import Hotel # Import the Booking model from models.py
from .models import Amenity

admin.site.register(Hotel)  # Register the Car model with the admin site
admin.site.register(Amenity)  # Register the Car model with the admin site
