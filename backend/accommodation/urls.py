from rest_framework import urlpatterns
from django.db import router
from rest_framework.routers import DefaultRouter
from .views import AccommodationView, LandlordAccommodationView


router = DefaultRouter()
router.register('my-accommodations', LandlordAccommodationView, basename='landlord-accommodations')
router.register('', AccommodationView, basename='accommodations')

urlpatterns = router.urls
