from django.http import response
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS

from .models import Message
from chat.models import Chat
from user.models import User
from .serializers import MessageSerializer


class MessageWritePermission(BasePermission):
    message = 'Editing Message is restricted to the user itself.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class MessageEditView(viewsets.ModelViewSet,
                            MessageWritePermission):
    permission_classes = [MessageWritePermission]
    serializer_class = MessageSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return generics.get_object_or_404(Message, pk=item)

    def get_queryset(self, *args, **kwargs):
        chat = Chat.objects.get(pk=self.request.query_params.get('chat', None))

        if chat is not None:
            return Message.objects.filter(chat=chat).order_by("date")
        else:
            return None

    def create(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.data.get('user'))
        chat = Chat.objects.get(pk=self.request.data.get('chat'))

        message = Message.objects.create(
            chat = chat,
            user = user,
            text = self.request.data.get('text')
        )
        serializer = MessageSerializer(message)

        return Response(serializer.data)