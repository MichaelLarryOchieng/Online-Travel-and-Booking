from django.db import models
from city.models import City
from django.core.files import File
from PIL import Image
from io import BytesIO

from django.conf import settings # To link to your CustomUser model
from django.core.exceptions import ValidationError
from django.utils import timezone

class Car(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    
    # Fields with sensible defaults
    year = models.IntegerField(default=2023)
    color = models.CharField(max_length=50, default='black')
    seats = models.IntegerField(default=5)
    luggage_capacity = models.IntegerField(default=2)
    fuel_type = models.CharField(max_length=50, default='petrol')
    transmission = models.CharField(max_length=50, default='automatic')
    
    # Boolean fields default to False
    air_conditioning = models.BooleanField(default=False)
    gps = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=False)
    child_seat = models.BooleanField(default=False)
    cruise_control = models.BooleanField(default=False)
    parking_sensors = models.BooleanField(default=False)
    heated_seats = models.BooleanField(default=False)
    sunroof = models.BooleanField(default=False)
    navigation_system = models.BooleanField(default=False)
    
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.company} - {self.model} ({self.city.name})"
    
    def get_absolute_url(self):
        return f"/{self.slug}/"

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(250, 200)):
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=90)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    

class CarBooking(models.Model):
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='car_bookings'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE, # Or models.PROTECT/SET_NULL if needed
        related_name='bookings'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # Will be calculated
    booking_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        start_str = self.start_date.strftime('%Y-%m-%d') if self.start_date else 'N/A'
        end_str = self.end_date.strftime('%Y-%m-%d') if self.end_date else 'N/A'
        return f"Booking for {self.car.name} ({start_str} to {end_str}) by {self.passenger.username}"

    def clean(self):
        # Basic validation
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after start date.")
            if self.start_date < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0): # Compare dates only
                 raise ValidationError("Start date cannot be in the past.")
        # More complex availability check could go here or in the serializer
        super().clean()

    def calculate_duration_days(self):
        if self.start_date and self.end_date:
            # Ensure comparison is date-based if time isn't relevant for pricing days
            start = self.start_date.date()
            end = self.end_date.date()
            duration = end - start
            # Calculate days, minimum 1 day even for same-day return
            days = duration.days + 1 # Add 1 because booking for 1 day means start/end on same day usually counts as 1
            return max(days, 1) # Ensure at least 1 day
        return 0


# Create your models here.

