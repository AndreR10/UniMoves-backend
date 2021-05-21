from django.db import models


CONTRACT_TYPES = [
    ('B', 'Biweekly'),
    ('Y', 'Yearly'),
    ('S', 'Semiannual'),
]


class RentalCondition(models.Model):
    accommodation = models.ForeignKey('accommodation.Accommodation',
                                      on_delete=models.CASCADE)
    contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPES)
    price_per_month = models.IntegerField()
    mininum_stay = models.IntegerField()
    expenses = models.BooleanField()
    cleaning_service = models.BooleanField()
    refund_policy = models.TextField(blank=True)
    safety_deposit = models.IntegerField()
