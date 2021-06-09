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
        queryset = Receipt.objects.all()
        user = User.objects.get(email=self.request.user)
        payment = self.request.query_params.get('payment', None)
        print(user)
        if user.is_landlord == True:
            print("entrei")
            queryset = queryset.filter(landlord_nif=user.nif)
        elif user.is_tenant == True:
            queryset = queryset.filter(tenant_nif=user.nif)

        if payment:
            payment = Payment.objects.get(pk=payment)
            queryset = queryset.filter(payment=payment)
        
        return queryset