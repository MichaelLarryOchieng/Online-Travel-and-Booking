from django.db import models
from accounts.models import CustomUser  # Import CustomUser
from flight.models import Flight, Seat # Import Flight and Seat
import uuid# Import uuid for unique booking reference

def generate_booking_reference():
    return str(uuid.uuid4()).upper()[:12]#

# booking/models.py
class Booking(models.Model):
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    seats_booked = models.IntegerField(default=0)  # Add this field
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_cancelled = models.BooleanField(default=False)

    #def __str__(self):
        #return f"Booking {self.id} for {self.passenger.email}"

    #def save(self, *args, **kwargs):
        #is_new = not self.pk
        #super().save(*args, **kwargs)


