from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from manufacturers.models import ManufacturerModel

# from.models import ManufacturerModel

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the product object"""

    name = serializers.CharField(allow_blank=True, allow_null=True)
    description= serializers.CharField(allow_blank=True, allow_null=True)
    image = serializers.ImageField() 
    price = serializers.CharField(allow_blank=True, allow_null=True)
    composition = serializers.CharField(allow_blank=True, allow_null=True)
    manufacturer = serializers.CharField(allow_blank=True, allow_null=True)
    quantity = serializers.CharField(allow_blank=True, allow_null=True)
    category = serializers.CharField(allow_blank=True, allow_null=True)
    create_date = serializers.DateField()

    class Meta:
        fields = ('id', 'name', 'password', "description", "image", "price", "composition", "manufacturer", "quantity", "category", "create_date")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'

class ManfacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManufacturerModel
        fields = '__all__'

class orderSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, allow_null=True)
    image = serializers.CharField(allow_blank=True, allow_null=True)
    ids = serializers.IntegerField(allow_null=True)
    quantity = serializers.IntegerField(allow_null=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        fields = ['name','image','ids','quantity', 'price', 'created_at']

class syncUserSerializer(serializers.Serializer):
    email = serializers.CharField(allow_blank=False, allow_null=False)
    password = serializers.CharField(allow_blank=False, allow_null=False)

    class Meta:
        fields = ['email', 'password']


    def create(self, validate_data):
        return MyDrugStocItem.objects.create(**validate_data)

class CreateOrderSerializer(serializers.Serializer):
    items = orderSerializer(many=True)

    class Meta:
        fields = ['name','image','ids','quantity', 'price', 'created_at']
