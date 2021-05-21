from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from accommodation.models import Accommodation

from .models import RentalCondition
from .serializers import RentalConditionSerializer


class RentalConditionWritePermission(BasePermission):
    message = "Editing Rental conditions is restricted to the landlord only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.accommodation.landlord == request.user


class RentalConditionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = RentalConditionSerializer
    queryset = RentalCondition.objects.all()


class LandlordRentalConditionView(viewsets.ModelViewSet, RentalConditionWritePermission):
    permission_classes = [RentalConditionWritePermission]
    serializer_class = RentalConditionSerializer

    
    def get_queryset(self, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.query_params.get('accommodation', None))

        if accommodation is not None:
            return RentalCondition.objects.filter(accommodation=accommodation)
        else:
            return None

    def create(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.data.get('accommodation'))

        rental_conditions = RentalCondition.objects.create(
            contract_type = self.request.data.get('contract_type'),
            price_per_month = self.request.data.get('price_per_month'),
            mininum_stay = self.request.data.get('mininum_stay'),
            expenses = self.request.data.get('expenses'),
            cleaning_service = self.request.data.get('cleaning_service'),
            refund_policy = self.request.data.get('refund_policy'),
            safety_deposit = self.request.data.get('safety_deposit'),
            accommodation = accommodation,
        )
        serializer = RentalConditionSerializer(rental_conditions)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.data.get('accommodation'))
        rental = RentalCondition.objects.get(accommodation=accommodation)
        data = self.request.data
        data.pop('accommodation')

        for key in data:
            setattr(accommodation, key, self.request.data.get(key))

        serializer = RentalConditionSerializer(rental, data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)