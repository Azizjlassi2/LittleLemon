from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from . import models
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','title','slug']

        def validate_title(self, value):
            return bleach.clean(value)
        
        def validate_slug(self, value):
            return bleach.clean(value)




class MenuItemSerializer(serializers.ModelSerializer):

    
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model  = models.MenuItem
        fields = ['id','title','price', 'stock','featured','category','category_id']
        extra_kwargs = {
            'price': {'min_value': 0.0},
            'stock': {'min_value': 0.0},
            # To make sure that the title field remains unique in the MenuItem table
            'title': {
                    'validators': [
                        UniqueValidator(
                        queryset=models.MenuItem.objects.all()
                    )
                ]
            }
        }
        def validate_title(self, value):
            return bleach.clean(value)


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"username","email"]


        def validate_username(self, value):
            return bleach.clean(value)



class CartSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = models.Cart
        fields = '__all__'
        extra_kwargs = {
            'quantity': {'min_value': 1.0},
            'unit_price': {'min_value': 1.0},
        }
        

    


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','user','delivery_crew','total','status']
        
        def validate_total(self,value):
            """
            `total` cannot be equal to 0 or negative

            """
            if value < 1.0:
                raise serializers.ValidationError("Total cannot be negative or equal to 0")


        


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        

        