from rest_framework import serializers

from .models import Payment
from lease.models import Lease

from allauth.account.adapter import get_adapter


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        return Payment.objects.create(
            payment_number=validated_data['payment_number'],
            lease=validated_data['lease'],
            tenant=validated_data['tenant'],
            landlord=validated_data['landlord'],
            landlord_iban=validated_data['landlord_iban'],
            amount=validated_data['amount'],
        )