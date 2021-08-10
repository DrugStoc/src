import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

def document_images_file_path(instance,  filename):
    """Generate file path for images """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('manufacturer', filename)


class ManufacturerModel(models.Model):
    """Model for list of manufacturers"""

    name = models.CharField(max_length=255, blank=True, default="")
    priority = models.IntegerField(default=0, blank=False)
    image = models.ImageField(null=True, upload_to=document_images_file_path, blank=True)

    class Meta:
        ordering = ('user__priority', )

    def __str__(self):
        return self.name
