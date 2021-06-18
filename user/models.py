import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def document_images_file_path(instance,  filename):
    """Generate file path for images """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/documents', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creating and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Creates and save a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    CHOICES = (
        ('private-patient', 'Private Patient'),
        ('pharmacy', 'Pharmacy'),
        ('doctors-office', 'Doctors Office'),
        ('clinic', 'Clinic'),
        ('hospital', 'Hospital'),
        ('nursing-home', 'Nursing Home'),
    )

    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    category = models.CharField(max_length=255, default="", choices = CHOICES)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255, default="")
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    erp_id = models.IntegerField(default=0, blank=False)
    erp_id_2 = models.IntegerField(default=0, blank=False)
    erp_access = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

class PhoneOtp(models.Model):

    def create_otp(self, phone_no, otp_code, **extra_fields):
        """Creating and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        otp = self.model(phone_no=self.phone_no, otp_code=self.otp_code **extra_fields)
        otp.save(using=self._db)

    phone_no = models.CharField(max_length=255, default="")
    otp_code = models.CharField(max_length=6, default="")
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0, blank=False)
    created_date = models.DateTimeField(default=now, blank=False)


    def __str__(self):
        return str(self.phone_no)

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True)
    discover = models.CharField(max_length=255, null=True)
    practice_license = models.ImageField(null=True, upload_to=document_images_file_path, blank=True,)
    premise_license = models.ImageField(null=True, upload_to=document_images_file_path, blank=True,)

    def __str__(self):
        return self.user.name