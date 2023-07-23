from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import View
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

# Create your views here.
class COrder(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
