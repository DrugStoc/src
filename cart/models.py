from django.db import models
from django.conf import settings
from django.utils.timezone import now





class CartItem(models.Model):
    """items in cart"""

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=555)
    ids = models.IntegerField(default=0, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(default=now, blank=False)
    is_checkedout = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_cart', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# class Address(models.Model):
#     """ delivery address """
#     date_created = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     street_address1 = models.CharField(max_length=255)
#     street_address2 = models.CharField(max_length=255, blank=True, null=True)
#     city = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     cart = models.ForeignKey('CartModel', related_name='cart', on_delete=models.CASCADE)
#     zip = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.user
