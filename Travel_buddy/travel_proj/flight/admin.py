from django.contrib import admin
from .models import Flight, Airport, Seat, SeatClass  # Import the Flight and Airport models
from city.models import City  # Import the City model


admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Seat)  # Register the City model if needed
admin.site.register(SeatClass)
 
# Register your models here.

