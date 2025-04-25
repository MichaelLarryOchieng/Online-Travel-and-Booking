from django.db import models
from city.models import City # Import the City model
from django.core.files import File
from PIL import Image# Import the Python Imaging Library (PIL) for image processing
from io import BytesIO# Import BytesIO for in-memory byte streams

class Attraction(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='attractions/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.name
  
    def get_absolute_url(self):
        return f"/{self.slug}/"
  
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

# Create your models here.
