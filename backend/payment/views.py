from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from user.models import User
from lease.models import Lease
from receipt.models import Receipt
from .models import Payment
from .serializers import PaymentSerializer
from receipt.serializers import ReceiptSerializer

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

    
class MakePaymentView(viewsets.ModelViewSet, PaymentWritePermission):
    permission_classes = [PaymentWritePermission]
    serializer_class = PaymentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Payment, pk=item)

    def get_queryset(self, *args, **kwargs):
        return Payment.objects.all() 

    def create(self, request, *args, **kwargs):
        data = self.request.data
        
        for payment in data:
            landlord = User.objects.get(pk=payment.get('landlord'))
            payment['landlord_iban'] = landlord.landlord_iban

        serializer = PaymentSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)


class MyPaymentView(viewsets.ModelViewSet, PaymentWritePermission):
    permission_classes = [PaymentWritePermission]
    serializer_class = PaymentSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Payment, pk=item)

    def get_queryset(self, *args, **kwargs):
        queryset = Payment.objects.all()
        user = User.objects.get(email=self.request.user)
        lease = self.request.query_params.get('lease', None)
        payment = self.request.query_params.get('payment', None)

        if lease:
            lease = Lease.objects.get(pk=self.request.query_params.get('lease'))
            queryset = queryset.filter(lease=lease)

        if payment:
            queryset = queryset.filter(pk=payment)

        if user.is_tenant == True:
            queryset = queryset.filter(tenant=user)
        else:
            queryset = queryset.filter(landlord=user)

        return queryset


    def update(self, request, *args, **kwargs):
        payment = Payment.objects.get(pk=self.kwargs['pk'])
        
        receipt = Receipt.objects.create(
            payment = payment,
            tenant_nif = payment.tenant.nif,
            landlord_nif = payment.landlord.nif
        )
        receipt_serializer = ReceiptSerializer(receipt)
        
        payment_serializer = PaymentSerializer(payment, data=self.request.data, partial=True)
        
        if payment_serializer.is_valid():
            payment_serializer.save()

            return Response(payment_serializer.data)
        
        return Response(payment_serializer.errors)