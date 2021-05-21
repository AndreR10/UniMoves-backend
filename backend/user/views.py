from django.http import response
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated, SAFE_METHODS
from .serializers import UserSerializer
from .models import User


class UserWritePermission(BasePermission):
    message = 'Editing User is restricted to the user itself.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return generics.get_object_or_404(User, slug=item)

    def get_queryset(self, *args, **kwargs):
        return User.objects.all()


class UserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return generics.get_object_or_404(User, slug=item)

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        if user is not None:
            return User.objects.filter(pk=user.pk)
        else:
            return None


class UserEditView(viewsets.ModelViewSet, UserWritePermission):
    permission_classes = [UserWritePermission]
    serializer_class = UserSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')

        return generics.get_object_or_404(User, slug=item)

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user)

        if user is not None:
            return User.objects.filter(pk=user.pk)
        else:
            return None

    def update(self, request, *args, **kwargs):
        user = User.objects.get(email=self.request.user)
    
        for key in self.request.data:
            setattr(user, key, self.request.data.get(key))

        serializer = UserSerializer(user)

        return Response(serializer.data)