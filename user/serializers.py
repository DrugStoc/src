from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Document

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""
    CHOICES = (
        ('private-patient', 'Private Patient'),
        ('pharmacy', 'Pharmacy'),
        ('doctors-office', 'Doctors Office'),
        ('clinic', 'Clinic'),
        ('hospital', 'Hospital'),
        ('nursing-home', 'Nursing Home'),
    )

    email = serializers.CharField(allow_blank=True, allow_null=True)
    # password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, allow_blank=True, allow_null=True)
    name = serializers.CharField(allow_blank=True, allow_null=True)
    first_name = serializers.CharField(allow_blank=True, allow_null=True)
    last_name = serializers.CharField(allow_blank=True, allow_null=True)
    category = serializers.ChoiceField(choices = CHOICES, allow_blank=False, allow_null=False)
    phone_no = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'password', 'first_name', 'last_name', 'category', 'phone_no', 'is_verified')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
        

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
            
        
        return user



class OtpSerializer(serializers.Serializer):
    """Serializer for verifying user otp"""

    otp = serializers.CharField(allow_blank=True, allow_null=True)
    phone_no = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        fields = ('otp', 'email', 'phone_no', 'password', 'pin_id')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            msg = ('Unable to autheticate with provided details')
            raise serializers.ValidationError(msg, code='authetication')

        attrs['user'] = user
        return attrs


class UploadDocumentSerializer(serializers.Serializer):
    """Serializer for uploading document"""
    user = UserSerializer(read_only=True)
    location = serializers.CharField(allow_blank=True, allow_null=True)
    discover = serializers.CharField(allow_blank=True, allow_null=True)
    practice_license = serializers.ImageField() 
    premise_license = serializers.ImageField() 

    class Meta:
        fields = ("id", "user", "location", 'discover', 'practice_license', 'premise_license')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return Document.objects.create(**validated_data)
