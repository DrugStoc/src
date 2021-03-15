import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

from manufacturers.models import ManufacturerModel
from categories.models import CategoryModel

def document_images_file_path(instance,  filename):
    """Generate file path for images """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/products', filename)


class ProductModel(models.Model):
    """Products model for all list of products"""

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=document_images_file_path, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(ManufacturerModel, related_name='manufacturer', on_delete=models.PROTECT)
    composition = models.TextField()
    category_name = models.ForeignKey(CategoryModel, related_name='category', on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0, blank=False)
    create_date = models.DateField(default=now, blank=False)

    def __str__(self):
        return self.name