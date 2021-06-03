from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from payment.models import Payment
from user.models import User
from lease.models import Lease
from .models import Receipt
from .serializers import ReceiptSerializer


class ReceiptWritePermission(BasePermission):
    message = "Editing Receipt is restricted to the user only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_landlord == True:
            return obj.landlord_nif == request.user.nif
        elif request.user.is_tenant == True:
            return obj.tenant_nif == request.user.nif


class ReceiptView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReceiptSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Receipt, pk=item)

    def get_queryset(self):
        user = User.objects.get(email=self.request.user)

        if user.is_landlord == True:
            return Receipt.objects.filter(landlord_nif=user.nif)
        elif user.is_tenant == True:
            return Receipt.objects.filter(tenant_nif=user.nif)

        payment = Payment.objects.filter(
            lease=self.request.query_params.get('lease', None)
        ).get(payment_number=self.request.query_params.get('payment_number', None))

        if payment is not None:
            return Receipt.objects.filter(payment=payment)
        else:
            return None