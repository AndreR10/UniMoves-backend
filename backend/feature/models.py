from django.db import models

SOLAR_ORIENTATION = [
    ("N", "North"),
    ("NE", "Northeast"),
    ("NW", "Northwest"),
    ("SE", "Southeast"),
    ("SW", "Southwest"),
    ("E", "East"),
    ("W", "West"),
]


class Feature(models.Model):
    accommodation = models.ForeignKey("accommodation.Accommodation",
                                      on_delete=models.CASCADE)
    area = models.IntegerField()
    occupancy = models.IntegerField()
    rooms = models.IntegerField()
    baths = models.IntegerField()
    lift = models.BooleanField()
    accessibility = models.BooleanField()
    ac = models.BooleanField()
    heater = models.BooleanField()
    outside_area = models.BooleanField()
    wifi = models.BooleanField()
    tv = models.BooleanField()
    energy_certificate = models.CharField(max_length=2, blank=True)
    smoking = models.BooleanField()
    guest_stay = models.BooleanField()
    pets = models.BooleanField()
    furnished = models.BooleanField(default=False)
    solar_orientation = models.CharField(max_length=2,
                                         choices=SOLAR_ORIENTATION)
