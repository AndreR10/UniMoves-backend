from .views import FeatureView, LandlordFeatureView
from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('accommodation-features', LandlordFeatureView, basename='accommodation-features')

urlpatterns = router.urls
