from django.db import models


class Receipt(models.Model):
    payment = models.ForeignKey('payment.Payment', on_delete=models.CASCADE)
    tenant_nif = models.IntegerField()
    landlord_nif = models.IntegerField()