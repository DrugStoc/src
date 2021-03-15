import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

class CategoryModel(models.Model):
    """Model for list of categories"""

    name = models.CharField(max_length=255, blank=True, default="")
    total_products = models.IntegerField(default=0, blank=False)
    create_date = models.DateField(default=now, blank=False)

    def __str__(self):
        return self.name