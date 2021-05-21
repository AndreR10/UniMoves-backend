from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from user.models import User
from lease.models import Lease
from receipt.models import Receipt
from .models import Payment
from .serializers import PaymentSerializer

from datetime import datetime


class PaymentWritePermission(BasePermission):
    message = "Editing Payment is restricted to the landlord only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_landlord == True:
            return obj.landlord_ == request.user
        elif request.user.is_tenant == True:
            return obj.tenant == request.user


class PaymentVisualizeView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Payment, pk=item)

    def get_queryset(self):
        lease = Lease.objects.get(pk=self.request.query_params.get('lease', None))

        if lease is not None:
            return Payment.objects.filter(lease=lease)
        else:
            return None

    
class PaymentView(viewsets.ModelViewSet, PaymentWritePermission):
    permission_classes = [PaymentWritePermission]
    serializer_class = PaymentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Payment, pk=item)

    def get_queryset(self, *args, **kwargs):
        return Payment.objects.all() 

    def create(self, request, *args, **kwargs):
        lease = Lease.objects.get(pk=self.request.data.get('lease'))

        payment = Payment.objects.create(
            lease = lease,
            tenant = lease.tenant,
            landlord = lease.landlord,
            landlord_iban = lease.landlord.landlord_iban,
            completed = True,
            amount = self.request.data.get('amount'),
        )
        serializer = PaymentSerializer(payment)

        return Response(serializer.data)


class LandlordPaymentView(viewsets.ModelViewSet, PaymentWritePermission):
    permission_classes = [PaymentWritePermission]
    serializer_class = PaymentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Payment, pk=item)

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
        lease = self.request.query_params.get('lease', None)

        if lease is not None:
            lease = Lease.objects.get(pk=self.request.query_params.get('lease'))

        if user is not None and lease is not None:
            return Payment.objects.filter(lease=lease).filter(landlord=user)
        if user is not None:
            return Payment.objects.filter(landlord=user)
        else:
            return None