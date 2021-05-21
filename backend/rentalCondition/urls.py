from .views import RentalConditionView, LandlordRentalConditionView
from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('accommodation-rental-conditions', LandlordRentalConditionView, basename='accommodation-rental-conditions')

urlpatterns = router.urls
