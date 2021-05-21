from rest_framework import serializers

from user.models import User
from .models import Accommodation


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'