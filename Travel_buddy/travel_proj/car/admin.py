from django.contrib import admin
from .models import Car,CarBooking # Import the Car model from models.py

admin.site.register(Car)  # Register the Car model with the admin site
admin.site.register(CarBooking)
# Register your models here.
