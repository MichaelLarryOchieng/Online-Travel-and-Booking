from django.db import models

class City(models.Model):

class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    airport_code = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.country}"
# Create your models here.
