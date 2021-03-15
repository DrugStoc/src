from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import CartItem

from user.serializers import UserSerializer


class AddCartSerializer(serializers.Serializer):

    name = serializers.CharField(allow_blank=True, allow_null=True)
    image = serializers.CharField(allow_blank=True, allow_null=True)
    ids = serializers.IntegerField(allow_null=True)
    quantity = serializers.IntegerField(allow_null=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['name','image','ids','quantity', 'price', 'user', 'is_checkedout', 'created_at']

    def create(self, validate_data):
        return CartItem.objects.create(**validate_data)


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','name','image','ids','quantity', 'price', 'created_at']