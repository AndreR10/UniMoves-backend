from rest_framework import serializers
from .models import RentalCondition


class RentalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalCondition
        fields = '__all__'