from datetime import date

from django.db import models

from random import randint

ACCOMMODATION_TYPES = [
    ('R', 'Room'),
    ('H', 'House'),
]

RATINGS_CHOICES = [
    (1, 'Very Poor'),
    (2, 'Poor'),
    (3, 'Fair'),
    (4, 'Good'),
    (5, 'Excellent'),
]


class Accommodation(models.Model):
    class Meta:
        ordering = ['publish_date']

    title = models.CharField(max_length=150)
    landlord = models.ForeignKey('user.User', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, blank=True)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=9)
    description = models.TextField(blank=True)
    accommodation_type = models.CharField(max_length=1,
                                          choices=ACCOMMODATION_TYPES)
    rating = models.IntegerField(null=True, choices=RATINGS_CHOICES)
    available = models.BooleanField(default=True)
    publish_date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(
            " ", "-") + "-" + self.accommodation_type + "-" + str(
                self.postal_code).lower()
        self.rating = randint(1, 5)

        return super(Accommodation, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
