from django.http import response
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS

from .models import Chat
from user.models import User
from .serializers import ChatSerializer


class ChatWritePermission(BasePermission):
    message = 'Editing Chat is restricted to the user itself.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_landlord == True:
            return obj.landlord == request.user
        elif request.user.is_tenant == True:
            return obj.tenant == request.user


class ChatEditView(viewsets.ModelViewSet,
                            ChatWritePermission):
    permission_classes = [ChatWritePermission]
    serializer_class = ChatSerializer
    
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return generics.get_object_or_404(Chat, pk=item)

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        if user is not None:
            if user.is_tenant == True:
                return Chat.objects.filter(tenant=user)
            elif user.is_landlord == True:
                return Chat.objects.filter(landlord=user)
        else:
            return None

    def create(self, request, *args, **kwargs):
        tenant = User.objects.get(email=self.request.data.get('tenant'))
        landlord = User.objects.get(email=self.request.data.get('landlord'))

        chat = Chat.objects.create(
            landlord = landlord,
            tenant = tenant,
        )
        serializer = ChatSerializer(chat)

        return Response(serializer.data)