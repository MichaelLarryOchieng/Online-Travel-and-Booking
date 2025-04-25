from django.db import models
from city.models import City  # Assuming you have a City model
from django.core.files import File
from PIL import Image
from io import BytesIO

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stars = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # 1 to 5 star rating
        default=3
    )
    amenities = models.ManyToManyField('Amenity', related_name='hotels', blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_image(self, request=None):
        if self.image:
            if request:
                return request.build_absolute_uri(self.image.url)
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
        try:
            img = Image.open(image)
            img.convert('RGB')
            img.thumbnail(size)

            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=90)

            thumbnail = File(thumb_io, name=image.name)
            return thumbnail
        except Exception as e:
            print(f"Error generating thumbnail: {e}")
            return None
        
class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
