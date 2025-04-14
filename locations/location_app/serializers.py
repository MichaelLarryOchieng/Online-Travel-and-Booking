from rest_framework import serializers
from .models import Locations
#serializers are used to convert complex data types to native python data types that can be rendered into JSON
#Serializers also validate the data that is passed to the API

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = "__all__"
# Create your serializers here.