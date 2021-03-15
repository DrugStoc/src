from django.db import models
from django.conf import settings
from django.utils.timezone import now





class MyDrugStocItem(models.Model):
    """items in cart"""

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=555)
    ids = models.IntegerField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(default=now, blank=False)
    is_Draft = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_mydrugstoc', on_delete=models.CASCADE)

    def __str__(self):
        return self.name