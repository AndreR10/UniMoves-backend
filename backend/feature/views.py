from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from accommodation.models import Accommodation

from .models import Feature
from .serializers import FeatureSerializer


class FeatureWritePermission(BasePermission):
    message = "Editing Features is restricted to the landlord only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.accommodation.landlord == request.user


class FeatureView(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()


class LandlordFeatureView(viewsets.ModelViewSet, FeatureWritePermission):
    permission_classes = [FeatureWritePermission]
    serializer_class = FeatureSerializer
    
    def get_queryset(self, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.query_params.get('accommodation', None))

        if accommodation is not None:
            return Feature.objects.filter(accommodation=accommodation)
        else:
            return None

    def create(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.data.get('accommodation'))

        features = Feature.objects.create(
            area = self.request.data.get('area'),
            occupancy = self.request.data.get('occupancy'),
            rooms = self.request.data.get('rooms'),
            baths = self.request.data.get('baths'),
            lift = self.request.data.get('lift'),
            accessibility = self.request.data.get('accessibility'),
            ac = self.request.data.get('ac'),
            heater = self.request.data.get('heater'),
            outside_area = self.request.data.get('outside_area'),
            wifi = self.request.data.get('wifi'),
            tv = self.request.data.get('tv'),
            energy_certificate = self.request.data.get('energy_certificate'),
            smoking = self.request.data.get('smoking'),
            guest_stay = self.request.data.get('guest_stay'),
            pets = self.request.data.get('pets'),
            furnished = self.request.data.get('furnished'),
            solar_orientation = self.request.data.get('solar_orientation'),
            accommodation = accommodation,
        )
        serializer = FeatureSerializer(features)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(slug=self.request.data.get('accommodation'))
        features = Feature.objects.get(accommodation=accommodation)
        data = self.request.data
        data.pop('accommodation')

        for key in data:
            setattr(accommodation, key, self.request.data.get(key))

        serializer = FeatureSerializer(features, data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

