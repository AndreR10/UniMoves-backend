from django.db import models

from datetime import date

class Payment(models.Model):
    lease = models.ForeignKey('lease.Lease', on_delete=models.CASCADE)
    tenant = models.ForeignKey('user.User',
                               related_name='tenant_payment',
                               on_delete=models.CASCADE)
    landlord = models.ForeignKey('user.User',
                                 related_name='landlord_payment',
                                 on_delete=models.CASCADE)
    landlord_iban = models.CharField(max_length=34)
    amount = models.IntegerField()
    completed = models.BooleanField(default=False)
    date_effected = models.DateField(default=date.today)