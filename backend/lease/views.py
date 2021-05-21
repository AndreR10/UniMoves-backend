from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LeaseSerializer
from .models import Lease
from user.models import User

from rest_framework.authtoken.models import Token


# Create your views here.
class ListLeases(ListAPIView):
    """
    View to list all leases in the system.
    * Requires token authentication.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer


class ListLandlordLeases(ListAPIView):
    """
    View to list all leases of a landlord in the system.
    * Requires token authentication. 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = LeaseSerializer

    queryset = Lease.objects.all()

    def get_queryset(self):
        return self.queryset.filter(landlord=self.request.user)


class DetailLandlordLease(RetrieveAPIView):
    """
    View to list all leases of a landlord in the system.
    * Requires token authentication. 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = LeaseSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Lease, pk=item)


class ListTenantLeases(ListCreateAPIView):

    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    def get_queryset(self):
        return Lease.objects.filter(tenant=self.request.user)


class DetailTenantLease(RetrieveUpdateDestroyAPIView):

    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # lookup_field = "id"

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Lease, pk=item)

    def get_queryset(self):
        return Lease.objects.filter(tenant=self.request.user)