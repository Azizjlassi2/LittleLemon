from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.MenuItem
        fields = "__all__"


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"username","email"]



class CartSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = models.Cart
        fields = '__all__'

    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','user','delivery_crew','total','status']

        


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'

        