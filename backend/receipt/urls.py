from django.db import router
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import ReceiptPaymentView, ReceiptView


router = DefaultRouter()
router.register('my-receipts', ReceiptView, basename='my-receipts')
router.register('payment-receipts', ReceiptPaymentView, basename='payment-receipts')

urlpatterns = router.urls