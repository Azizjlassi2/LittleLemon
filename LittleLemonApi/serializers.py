from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User , Group
from . import models
from decimal import Decimal
import bleach

import rest_framework.serializers as serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
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
    category = CategorySerializer(read_only=True) #read_only=True -> Not included in serialization

    class Meta:
        model  = models.MenuItem
        fields = ['id','title','price', 'stock','featured','category','category_id']
        extra_kwargs = {
            'price': {'min_value': Decimal()},
            'stock': {'min_value': Decimal()},
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


class UserManagerGroupSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id',"username","email","groups"]
        read_only_fields = ['groups']
        extra_kwargs = {'password': {'write_only': True}}
        depth=1


        def validate_username(self, value):
            return bleach.clean(value)
   



class UserDeliveryGroupSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(read_only=True)
    

    class Meta:
        model = User
        fields = ['id',"username","email","password","groups"]
        read_only_fields = ['groups']
        extra_kwargs = {'password': {'write_only': True}}
        depth=1

        def validate_username(self, value):
            return bleach.clean(value)
   

class CartSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = models.Cart
        fields = '__all__'
        extra_kwargs = {
            'quantity': {'min_value':Decimal(1)},
            'unit_price': {'min_value': Decimal(1)},
        }

        def valide_price(self,value):
            """
            `price` must be equal to `unit_price` * `quantity`

            """
            if not value == self.model.unit_price * self.model.quantity :
                raise serializers.ValidationError(" `price` must be equal to `unit_price` * `quantity`")
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','user','delivery_crew','total','status']
        
        def validate_total(self,value):
            """
            `total` cannot be equal to 0 or negative

            """
            if value < Decimal(1.0):
                raise serializers.ValidationError("Total cannot be negative or equal to 0")

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        

        