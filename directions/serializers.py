from rest_framework import serializers
from .models import SubwayStationtime

class DirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubwayStationtime
        fields = '__all__'