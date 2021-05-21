from rest_framework import serializers

from .models import Payment

from allauth.account.adapter import get_adapter


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'