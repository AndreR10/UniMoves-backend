from django.urls import path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import ListLandlordLeases, ListLeases, DetailLandlordLease, ListTenantLeases, DetailTenantLease

urlpatterns = [
    path('', ListLeases.as_view(), name="list-leases"),
    path('landlord/',
         ListLandlordLeases.as_view(),
         name="list-landlord-leases"),
    path('landlord/lease/<str:pk>',
         DetailLandlordLease.as_view(),
         name="detail-landlord-lease"),
    path('tenant/', ListTenantLeases.as_view(), name="list-tenant-leases"),
    path('tenant/lease/<str:pk>',
         DetailTenantLease.as_view(),
         name="detail-tenant-lease")
]
