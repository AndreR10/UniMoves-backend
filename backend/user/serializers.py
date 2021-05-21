from django.db.models import fields
from .models import User, GENDER_CHOICES, TENANT_ROLES, LANDLORD_TYPES, RATINGS_CHOICES
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from datetime import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email',
            'password',
            'gender',
            'picture',
            'birth_date',
            'phone_number',
            'educational_institution',
            'role',
            'type_landlord',
            'landlord_iban',
            'nif',
            'rating',
            'slug',
            'is_tenant',
            'is_landlord',
        )


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(max_length=128)
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    phone_number = serializers.CharField(max_length=9)
    educational_institution = serializers.CharField(allow_blank=True,
                                                    max_length=128)
    role = serializers.ChoiceField(allow_null=True, choices=TENANT_ROLES)
    type_landlord = serializers.ChoiceField(allow_null=True,
                                            choices=LANDLORD_TYPES)
    landlord_iban = serializers.CharField(allow_blank=True, max_length=34)
    nif = serializers.CharField(max_length=9)
    rating = serializers.ChoiceField(allow_null=True, choices=RATINGS_CHOICES)
    is_tenant = serializers.BooleanField()
    is_landlord = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'birth_date', 'gender',
                  'phone', 'educational_institution', 'role', 'type_landlord',
                  'landlord_iban', 'nif', 'rating', 'is_tenant', 'is_landlord')

    def get_cleaned_data(self):
        return {
            'password1':
            self.validated_data.get('password1', ''),
            'password2':
            self.validated_data.get('password2', ''),
            'email':
            self.validated_data.get('email', ''),
            'full_name':
            self.validated_data.get('full_name', ''),
            'birth_date':
            self.validated_data.get('birth_date', ''),
            'gender':
            self.validated_data.get('gender', ''),
            'phone_number':
            self.validated_data.get('phone_number', ''),
            'educational_institution':
            self.validated_data.get('educational_institution', ''),
            'role':
            self.validated_data.get('role', ''),
            'type_landlord':
            self.validated_data.get('type_landlord', ''),
            'landlord_iban':
            self.validated_data.get('landlord_iban', ''),
            'nif':
            self.validated_data.get('nif', ''),
            'rating':
            self.validated_data.get('rating', ''),
            'is_tenant':
            self.validated_data.get('is_tenant', ''),
            'is_landlord':
            self.validated_data.get('is_landlord', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.full_name = self.cleaned_data.get('full_name')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.gender = self.cleaned_data.get('gender')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.educational_institution = self.cleaned_data.get(
            'educational_institution')
        user.role = self.cleaned_data.get('role')
        user.type_landlord = self.cleaned_data.get('type_landlord')
        user.landlord_iban = self.cleaned_data.get('landlord_iban')
        user.nif = self.cleaned_data.get('nif')
        user.rating = self.cleaned_data.get('rating')
        user.is_tenant = self.cleaned_data.get('is_tenant')
        user.is_landlord = self.cleaned_data.get('is_landlord')
        user.save()
        adapter.save_user(request, user, self)

        return user