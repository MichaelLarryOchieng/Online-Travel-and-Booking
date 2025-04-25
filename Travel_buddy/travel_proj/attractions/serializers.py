from rest_framework import serializers
from .models import Attraction

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'get_absolute_url', 'city', 'address', 'description', 'price', 'get_image', 'get_thumbnail']
#         # fields = '__all__'  # This will include all fields in the model