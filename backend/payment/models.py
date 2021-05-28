from django.db import models

from datetime import date

class Payment(models.Model):
    payment_number = models.IntegerField()
    lease = models.ForeignKey('lease.Lease', on_delete=models.CASCADE)
    tenant = models.ForeignKey('user.User',
                               related_name='tenant_payment',
                               on_delete=models.CASCADE)
    landlord = models.ForeignKey('user.User',
                                 related_name='landlord_payment',
                                 on_delete=models.CASCADE)
    landlord_iban = models.CharField(blank=True, max_length=34)
    amount = models.IntegerField()
    completed = models.BooleanField(default=False)
    date_effected = models.DateField(null=True, blank=True)