from rest_framework import serializers
from .models import Hotel, Amenity
from city.serializers import CitySerializer  # Import CitySerializer
from city.models import City

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']

class HotelSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    city_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'city',
            'city_id',
            'address',
            'description',
            'stars',
            'amenities',
            'price_per_night',
            'availability',
            'image',
            'thumbnail',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'thumbnail']

    def create(self, validated_data):
        city_id = validated_data.pop('city_id')
        try:
            city_obj = City.objects.get(pk=city_id)
        except City.DoesNotExist:
            raise serializers.ValidationError({"city_id": "City does not exist."})
        hotel = Hotel.objects.create(city=city_obj, **validated_data)
        return hotel

    def update(self, instance, validated_data):
        city_id = validated_data.pop('city_id', None)
        if city_id:
            try:
                city_obj = City.objects.get(pk=city_id)
                instance.city = city_obj
            except City.DoesNotExist:
                raise serializers.ValidationError({"city_id": "City does not exist."})

        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.price_per_night = validated_data.get('price_per_night', instance.price_per_night)
        instance.availability = validated_data.get('availability', instance.availability)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance
