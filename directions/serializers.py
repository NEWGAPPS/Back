from rest_framework import serializers
from .models import SubwayStation

class DirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubwayStation
        fields = '__all__'