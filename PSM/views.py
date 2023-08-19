from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Product, Order, Customer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import ProductSerializer, OrderSerializer, CustomerSerializer

# Create your views here.
class OrderView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        myorders = []
        for order in orders:
            tmp = OrderSerializer(order)
            myorders.append(tmp.data)
        return Response(myorders)
    def post(self, request):
        total = 0
        myitems = []
        for item in request.data["items"]:
            try:
                tmpitem = Product.objects.get(pname=item["product"])
                tmp = ProductSerializer(tmpitem).data
                myitem = { "product": tmp["pname"], "quantity": item["quantity"], "price": tmp["pprice"] }
                total += tmp["pprice"] * item["quantity"]
                myitems.append(myitem)
            except:
                continue
        total += 100 #delivery charges
        order = Order.objects.create(name=request.data["name"],
                                     address=request.data["address"],
                                     contact=request.data["contact"],
                                     chat=request.data["chat"],
                                     total=total,
                                     items=myitems,
                                     user=request.user)
        return Response(OrderSerializer(order).data)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = authenticate(request, username=request.data["username"], password=request.data["password"])
        if user is None:
            return Response({'error': 'wrong credentials or user not found'})
        token, created = Token.objects.get_or_create(user=user)
        return Response({"TOKEN": token.key})

class Profile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        customer = Customer.objects.get(user=user)
        try:
            user.first_name = request.data["fname"]
        except:
            pass
        try:
            user.last_name = request.data["lname"]
        except:
            pass
        try:
            customer.address = request.data["address"]
        except:
            pass
        user.save()
        customer.save()
        return Response(CustomerSerializer(customer).data)


class ProductView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        if request.user.is_staff is True:
            product = Product.objects.create(pname=request.data['name'],
                                             pprice=request.data['price'],
                                             ptag=request.data['tag'],
                                             available=request.data['available'])
            return Response(ProductSerializer(product).data)
        else:
            return Response({'error': 'not allowed'})
        
    def get(self, request):
        products = Product.objects.all()
        productlist = []
        for product in products:
            productlist.append(ProductSerializer(product).data)
        return Response(productlist)

class UpdateProductView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
    def put(self, request):
        updated = False
        product = Product.objects.get(pname=request.data["name"])
        if product is not None:
            try:
                product.pname = request.data["newname"]
                updated = True
            except:
                pass
            try:
                product.pprice = request.data["price"]
                updated = True
            except:
                pass
            try:
                product.available = request.data["available"]
                updated = True
            except:
                pass
            if updated is True:
                product.save()
            return Response(ProductSerializer(product).data)

class AdminAppView(APIView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication, )
    def get(self, request):
        return Response({"response": 'true'})

class SignUpView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer