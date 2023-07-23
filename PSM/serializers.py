from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pname', 'pprice', 'ptag', 'available']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()
    class Meta:
        model = Order
        fields = "__all__"