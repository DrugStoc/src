from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import MyDrugStocItem

# from user.serializers import UserSerializer

class myDrugStocSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, allow_null=True)
    image = serializers.CharField(allow_blank=True, allow_null=True)
    ids = serializers.IntegerField(allow_null=True)
    quantity = serializers.IntegerField(allow_null=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = MyDrugStocItem
        fields = ['name','image','ids','quantity', 'price', 'created_at']


    def create(self, validate_data):
        return MyDrugStocItem.objects.create(**validate_data)



class CreateDraftSerializer(serializers.Serializer):
    items = myDrugStocSerializer(many=True)

    class Meta:
        model = MyDrugStocItem
        fields = ['name','image','ids','quantity', 'price', 'created_at']


class DraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyDrugStocItem
        fields = ['id', 'name','image','ids','quantity', 'price']
