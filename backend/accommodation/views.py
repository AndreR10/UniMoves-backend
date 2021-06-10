from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission

from user.models import User
from feature.models import Feature
from rentalCondition.models import RentalCondition

from .models import ACCOMMODATION_TYPES, RATINGS_CHOICES, Accommodation
from .serializers import AccommodationSerializer


class AccommodationWritePermission(BasePermission):
    message = "Editing Accommodations is restricted to the landlord only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.landlord == request.user


class AccommodationView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccommodationSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Accommodation, slug=item)

    def get_queryset(self):
        queryset = Accommodation.objects.all()
        queryset = queryset.filter(available=True)

        # Accommodation filters
        location = self.request.query_params.get("location", None)
        accommodation_type = self.request.query_params.get("type", None)
        rating = self.request.query_params.get("rating", None)
        publish_date = self.request.query_params.get("recent", None)

        # Feature filters
        start_area = self.request.query_params.get("start-area", None)
        end_area = self.request.query_params.get("end-area", None)
        occupancy = self.request.query_params.get("occupancy", None)
        rooms = self.request.query_params.get("rooms", None)
        lift = self.request.query_params.get("lift", None)
        accessibility = self.request.query_params.get("accessibility", None)
        ac = self.request.query_params.get("ac", None)
        heater = self.request.query_params.get("heater", None)
        outside_area = self.request.query_params.get("outside", None)
        wifi = self.request.query_params.get("wifi", None)
        tv = self.request.query_params.get("tv", None)
        smoking = self.request.query_params.get("smoking", None)
        guest_stay = self.request.query_params.get("guests", None)
        pets = self.request.query_params.get("pets", None)
        solar_orientation = self.request.query_params.get("orientation", None)
        furnished = self.request.query_params.get("furnished", None)

        # Rental Condition filters
        contract_type = self.request.query_params.get("contract", None)
        start_price = self.request.query_params.get("start-price", None)
        end_price = self.request.query_params.get("end-price", None)
        expenses = self.request.query_params.get("expenses", None)
        cleaning_service = self.request.query_params.get("cleaning", None)

        if location:
            queryset = queryset.filter(location=location)
        if accommodation_type:
            queryset = queryset.filter(accommodation_type=accommodation_type)
        if rating:
            queryset = queryset.filter(rating=rating)
        if publish_date:
            queryset = queryset.order_by("-publish_date")

        for accommodation in queryset:
            if Feature.objects.filter(accommodation=accommodation.pk).exists() and RentalCondition.objects.filter(accommodation=accommodation.pk).exists():
                features = Feature.objects.get(accommodation=accommodation)
                rental_conditions = RentalCondition.objects.get(accommodation=accommodation)

                if start_area and end_area:
                    if features.area not in range(int(start_area), int(end_area)):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if occupancy:
                    if features.occupancy != int(occupancy):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if rooms:
                    if features.rooms != int(rooms):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if lift:
                    if features.lift != bool(lift):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if furnished:
                    if features.furnished != bool(furnished):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if accessibility:
                    if features.accessibility != bool(accessibility):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if ac:
                    if features.ac != bool(ac):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if heater:
                    if features.heater != bool(heater):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if outside_area:
                    if features.outside_area != bool(outside_area):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if wifi:
                    if features.wifi != bool(wifi):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if tv:
                    if features.tv != bool(tv):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if smoking:
                    if features.smoking != bool(smoking):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if guest_stay:
                    if features.guest_stay != bool(guest_stay):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if pets:
                    if features.pets != bool(pets):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if solar_orientation:
                    if features.solar_orientation != solar_orientation:
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue

                if contract_type:
                    if rental_conditions.contract_type != contract_type:
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if start_price and end_price:
                    if rental_conditions.price_per_month not in range(int(start_price), int(end_price)):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if expenses:
                    if rental_conditions.expenses != bool(expenses):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue
                if cleaning_service:
                    if rental_conditions.cleaning_service != bool(cleaning_service):
                        queryset = queryset.exclude(pk=accommodation.pk)
                        continue

        return queryset


class LandlordAccommodationView(viewsets.ModelViewSet, AccommodationWritePermission):
    permission_classes = [AccommodationWritePermission]
    serializer_class = AccommodationSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get("pk")

        return generics.get_object_or_404(Accommodation, slug=item)

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        if user is not None:
            return Accommodation.objects.filter(landlord=user)
        else:
            return None

    def create(self, request, *args, **kwargs):
        landlord = User.objects.get(email=self.request.data.get('landlord'))

        accommodation = Accommodation.objects.create(
            title = self.request.data.get('title'),
            landlord = landlord,
            address = self.request.data.get('address'),
            location = self.request.data.get('location'),
            postal_code = self.request.data.get('postal_code'),
            description = self.request.data.get('description'),
            accommodation_type = self.request.data.get('accommodation_type'),
        )
        serializer = AccommodationSerializer(accommodation)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = self.request.data
        user = User.objects.get(pk=self.request.data.get('landlord'))
        accommodation = Accommodation.objects.filter(landlord=user).get(slug=self.request.data.get('slug'))
        
        data.pop('slug')
        
        serializer = AccommodationSerializer(accommodation, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    

        
