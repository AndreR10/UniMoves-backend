from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import PaymentVisualizeView, PaymentView, LandlordPaymentView


router = DefaultRouter()
router.register('make-payments', PaymentView, basename='make-payments')
router.register('my-payments', LandlordPaymentView, basename='my-payments')
router.register('lease-payments', PaymentVisualizeView, basename='lease-payments')

urlpatterns = router.urls
