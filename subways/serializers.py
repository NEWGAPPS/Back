from rest_framework import serializers
from .models import Subway

class SubwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subway
        fields = '__all__'
