from django.core.management.base import BaseCommand
from city.models import City
import geocoder

class Command(BaseCommand):
    help = 'Geocodes cities that are missing latitude and longitude'

    def handle(self, *args, **options):
        headers = {'User-Agent': 'TravelBuddy/0.0 (ochiengmichaellarry@gmail.com)'}  # Replace with your app details
        cities = City.objects.all()
        for city in cities:
            if not city.latitude or not city.longitude:
                g = geocoder.osm(f"{city.name}, {city.country}", headers=headers)
                if g.ok:
                    city.latitude = g.latlng[0]
                    city.longitude = g.latlng[1]
                    city.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully geocoded {city.name}: {city.latitude}, {city.longitude}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Could not geocode {city.name} - {g.status_code}: {g.reason}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipping {city.name} (coordinates already exist)'))

        self.stdout.write(self.style.SUCCESS('Geocoding process completed.'))