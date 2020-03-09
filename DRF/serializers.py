from rest_framework import serializers
from .models import ProductModel

class ProductSerializers(serializers.Serializer):
    no          = serializers.IntegerField()
    name        = serializers.CharField(max_length=30)
    price       = serializers.FloatField()
    quantity    = serializers.IntegerField()

    def create(self, validated_data):
        return ProductModel.objects.create(**validated_data)