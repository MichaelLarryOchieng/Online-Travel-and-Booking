from django.db import models
from city.models import City

# The Airport model
class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    code = models.CharField(max_length=3, default='XXX')  # Example: "LAX", "JFK"

    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    slug = models.SlugField()
    departure_airport = models.ForeignKey(Airport, related_name='departing_flights', on_delete=models.CASCADE, null=True)  # Added null=True
    arrival_airport = models.ForeignKey(Airport, related_name='arriving_flights', on_delete=models.CASCADE, null=True)  # Added null=True
    # ... other fields ...
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_city = models.ForeignKey(City, related_name='departing_flights', on_delete=models.CASCADE) #ADDED
    arrival_city = models.ForeignKey(City, related_name='arriving_flights', on_delete=models.CASCADE) #ADDED
    airline = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['departure_time']  # Default ordering by departure date

    def __str__(self):
        return f"{self.flight_number} - {self.departure_city.name} to {self.arrival_city.name}"

    def get_absolute_url(self):
        return f"/{self.slug}/"

class SeatClass(models.Model):
    name = models.CharField(max_length=50)
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Seat(models.Model):
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  # Track seat availability

    def __str__(self):
        return f"{self.seat_number} ({self.seat_class.name})"