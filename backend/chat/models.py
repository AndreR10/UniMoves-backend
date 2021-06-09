from django.db import models

from datetime import date

class Chat(models.Model):
    landlord = models.ForeignKey('user.User',
                                on_delete=models.CASCADE,
                                related_name='landlord_chat')
    tenant = models.ForeignKey('user.User',
                                on_delete=models.CASCADE,
                                related_name='tenant_chat')
    date = models.DateField(default=date.today)
    viewedLandlord = models.BooleanField(default=False)
    viewedTenant = models.BooleanField(default=False)