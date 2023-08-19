from rest_framework import serializers
from .models import Product, Order, Customer
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pname', 'pprice', 'ptag', 'available']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.JSONField()
    chat  = serializers.JSONField()
    class Meta:
        model = Order
        fields = "__all__"

class UserSerialzer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerialzer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    class Meta:
        model = Customer
        fields = ['user', 'address']