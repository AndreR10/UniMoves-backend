from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date

from random import randint

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]
TENANT_ROLES = [
    ('STD', 'Student'),
    ('TCH', 'Teacher'),
    ('RCH', 'Researcher'),
]
LANDLORD_TYPES = [
    ('PART', 'Particular'),
    ('AGEN', 'Agency'),
]
RATINGS_CHOICES = [
    (1, 'Very Poor'),
    (2, 'Poor'),
    (3, 'Fair'),
    (4, 'Good'),
    (5, 'Excellent'),
]


class User(AbstractUser):
    full_name = models.CharField(blank=True, max_length=128)
    birth_date = models.DateField(default=date.today)
    picture = models.ImageField(upload_to="user_pictures",
                                verbose_name="Profile Picture",
                                blank=True)
    gender = models.CharField(blank=True, max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(blank=True, max_length=9)
    educational_institution = models.CharField(blank=True, max_length=128)
    role = models.CharField(null=True, max_length=3, choices=TENANT_ROLES)
    landlord_iban = models.CharField(blank=True, max_length=34)
    nif = models.CharField(max_length=9, default=000000000)
    role = models.CharField(null=True, max_length=3, choices=TENANT_ROLES)
    type_landlord = models.CharField(null=True,
                                     max_length=4,
                                     choices=LANDLORD_TYPES)
    rating = models.IntegerField(null=True, choices=RATINGS_CHOICES)
    slug = models.SlugField(max_length=250, blank=True)
    is_tenant = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_landlord:
            self.slug = self.full_name.replace(
                " ", "-") + "-" + self.type_landlord.lower()
            self.rating = randint(1, 5)
        elif self.is_tenant:
            self.slug = self.full_name.replace(" ",
                                               "-") + "-" + self.role.lower()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
