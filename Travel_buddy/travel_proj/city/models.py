from django.db import models
from django.core.files import File
from PIL import Image
from io import BytesIO
from geopy.geocoders import Nominatim  # Import the geocoder
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cities/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)  # Add latitude field
    longitude = models.FloatField(blank=True, null=True) # Add longitude field

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

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

    def geocode(self):
        geolocator = Nominatim(user_agent="your_app_name") # Replace 'your_app_name'
        try:
            location = geolocator.geocode(f"{self.name}, {self.country}", exactly_one=True, timeout=10)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
                self.save()
            else:
                print(f"Could not geocode: {self.name}, {self.country}")
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding service error for {self.name}, {self.country}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during geocoding for {self.name}, {self.country}: {e}")

    def save(self, *args, **kwargs):
        # Geocode if latitude or longitude are not already set
        if self.latitude is None or self.longitude is None:
            self.geocode()
        super().save(*args, **kwargs)

