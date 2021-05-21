from django.db import models
from datetime import date


class Lease(models.Model):
    accommodation = models.ForeignKey('accommodation.Accommodation',
                                      on_delete=models.CASCADE)
    tenant = models.ForeignKey('user.User',
                               related_name='tenant_lease',
                               on_delete=models.CASCADE)
    landlord = models.ForeignKey('user.User',
                                 related_name='landlord_lease',
                                 on_delete=models.CASCADE)
    begin_date = models.DateField(default=date.today)
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)
