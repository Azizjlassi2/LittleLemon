from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group
from .models import*
from .serializers import *
from rest_framework.permissions import IsAuthenticated








class MenuItemsView(APIView):
    
    permission_classes = [IsAuthenticated]
   
    def get(self,request):
        # Query
        items = MenuItem.objects.all()

        # Filtering 
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        title_name = request.query_params.get('title')
        featured_option = request.query_params.get('featured')

        if category_name:
            items = MenuItem.objects.filter(category__title=category_name)
        if to_price:
            items = MenuItem.objects.filter(price__lte=to_price)
        if title_name:
            items = MenuItem.objects.filter(title=title_name)
        if featured_option:
            items = MenuItem.objects.filter(featured=featured_option)
        
        
        # Serialization
        serialized_items = MenuItemSerializer(items,many=True)
        return Response(serialized_items.data,status.HTTP_200_OK)


    def post(self,request):
        if request.user.groups.filter(name="Manager").exists():
            serialzed_item = MenuItemSerializer(data=request.data)
            if serialzed_item.is_valid():
                serialzed_item.save()
                return Response(serialzed_item.data,status.HTTP_201_CREATED)
            else:
                return Response(serialzed_item.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_403_FORBIDDEN)

class MenuItemView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        item = get_object_or_404(MenuItem,pk = id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data,status.HTTP_200_OK)

    def put(self,request,id):
        
        if request.user.groups.filter(name="Manager").exists():
            item = get_object_or_404(MenuItem,pk = id)
            serialized_item = MenuItemSerializer(item,data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_item.data,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id):

        if request.user.groups.filter(name="Manager").exists():
            item = get_object_or_404(MenuItem,pk = id)
            message = f"MenuItem {item.id} : {item.title} deleted !"
            item.delete()
            return Response(message,status.HTTP_200_OK)
        return Response(status.HTTP_403_FORBIDDEN)
    
       

class ManagerGroupsView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        users = User.objects.filter(groups__name__in =["Manager"])
        serialized_users = UserGroupSerializer(users,many=True)
        return Response(serialized_users.data,status.HTTP_200_OK)
    

    def post(self,request):
        if request.user.groups.filter(name="Manager").exists():
            
            serialized_user = UserGroupSerializer(data=request.data)
            if serialized_user.is_valid():
                serialized_user.save()
                manager_group = Group.objects.get(name="Manager")
                manager_group.user_set.add(serialized_user.data["id"])
                manager_group.save()
                return Response(serialized_user.data,status.HTTP_201_CREATED)
            else:
                return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status.HTTP_403_FORBIDDEN)

class ManagerGroupView(APIView):
    
    permission_classes = [IsAuthenticated]
    group_manager_id =  manager_group = Group.objects.get(name="Manager").pk


    def get(self,request,id):
        user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
        
        serialized_user = UserGroupSerializer(user)
        return Response(serialized_user.data,status.HTTP_200_OK)

    def put(self,request,id):
        
        if request.user.groups.filter(name="Manager").exists():
            
            user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
            print(user)
            serialized_user = UserGroupSerializer(user,data=request.data)
            print(serialized_user)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_user.data,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id):

        if request.user.groups.filter(name="Manager").exists():
            user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
            message = f"User {user.id} : {user.username} deleted !"
            user.delete()
            return Response(message,status.HTTP_200_OK)
        return Response(status.HTTP_403_FORBIDDEN)
    

    
class DeliveryCrewGroupsView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        users = User.objects.filter(groups__name__in =["Delivery Crew"])
        serialized_users = UserGroupSerializer(users,many=True)
        return Response(serialized_users.data,status.HTTP_200_OK)
    

    def post(self,request):
        if request.user.groups.filter(name="Manager").exists():
            
            serialized_user = UserGroupSerializer(data=request.data)
            if serialized_user.is_valid():
                serialized_user.save()
                delivery_crew_group = Group.objects.get(name="Delivery Crew")
                delivery_crew_group.user_set.add(serialized_user.data["id"])
                delivery_crew_group.save()
                return Response(serialized_user.data,status.HTTP_201_CREATED)
            else:
                return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status.HTTP_403_FORBIDDEN)

class DeliveryCrewGroupView(APIView):
    
    permission_classes = [IsAuthenticated]
    delivery_crew_id =   Group.objects.get(name="Delivery Crew").pk


    def get(self,request,id):
        user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
        
        serialized_user = UserGroupSerializer(user)
        return Response(serialized_user.data,status.HTTP_200_OK)

    def put(self,request,id):
        
        if request.user.groups.filter(name="Manager").exists():
            
            user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
            print(user)
            serialized_user = UserGroupSerializer(user,data=request.data)
            print(serialized_user)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_user.data,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id):

        if request.user.groups.filter(name="Manager").exists():
            user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
            message = f"User {user.id} : {user.username} deleted !"
            user.delete()
            return Response(message,status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_403_FORBIDDEN)
    

class CartsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
       
        carts = Cart.objects.filter(user=request.user.id)

        if request.user.groups.filter(name="Manager").exists():
            # For Administration And Data Science Features 
            # Filtering 
            gt_quantity = request.query_params.get('quantity')
            gt_price = request.query_params.get('price')
            
            

            if gt_quantity:
                carts = Cart.objects.filter(quantity__gte=gt_quantity)
            if gt_price:
                carts = Cart.objects.filter(price__gte=gt_price)

        serialized_carts = CartSerializer(carts,many=True)
        return Response(serialized_carts.data,status.HTTP_200_OK)
    
    def post(self,request):
      
        data = request.data.copy()
        data["user"] = f"{request.user.id}"
        
        
        serialized_cart = CartSerializer(data=data)
        print(serialized_cart)
        if serialized_cart.is_valid():
            serialized_cart.save()
            
            return Response(serialized_cart.data,status.HTTP_201_CREATED)
        else:
            return Response(serialized_cart.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        carts = Cart.objects.filter(user=request.user.id)
        for cart in carts:
            cart.delete()
        return Response(status.HTTP_204_NO_CONTENT)
        
class OrdersView(APIView):

    permissions_classes = [IsAuthenticated]

    def get(self,request) -> Response:
        """
        Returns all orders with order items created by this user

        """
        # Query

        if request.user.groups.filter(name="Manager").exists():

            orders = Order.objects.all()

        elif request.user.groups.filter(name="Delivery Crew").exists():

            orders = Order.objects.filter(delivery_crew=request.user.id)

        else:
            orders = Order.objects.filter(user=request.user.id)
        

        # Filtering
        gt_quantity = request.query_params.get('quantity')
        gt_total = request.query_params.get('total')
        status_option = request.query_params.get('status')
        lt_date = request.query_params.get('date')

        if gt_quantity:
            orders= orders.filter(quantity__gte=gt_quantity)

        if gt_total:
            orders = orders.filter(total__gte=gt_total)
        if status_option:
            orders = orders.filter(status=status_option)
        if lt_date:
            orders = orders.filter(date__lte=lt_date)



        serialized_orders = OrderSerializer(orders,many=True)
        return Response(serialized_orders.data,status.HTTP_200_OK)
    

    def post(self,request) -> Response :


        # Creates a new order item for the current user. 
        serialized_order = OrderSerializer(data=request.data)
        if serialized_order.is_valid():           
            serialized_order.save()

            order = get_object_or_404(Order,user=request.user.id)


        # Gets current cart items from the cart  and adds those items to the order items table. 
            carts = Cart.objects.filter(user=request.user.id)

            for cart in carts:

                new_order_item = OrderItem()
                new_order_item.order= order
                new_order_item.menuitem = cart.menuitem
                new_order_item.quantity = cart.quantity
                new_order_item.unit_price = cart.unit_price
                new_order_item.save()

            #Then deletes all items from the cart for this user.
                cart.delete()
            return Response(serialized_order.data,status.HTTP_201_CREATED)
        return Response(serialized_order.errors,status.HTTP_400_BAD_REQUEST)

class OrderView(APIView):
       
    permissions_classes = [IsAuthenticated]

    def get(self,request,id):


        order = get_object_or_404(Order,id=id)
        order_items = OrderItem.objects.filter(order=order)
        if order.user.pk == request.user.id:
            serialized_order_items = OrderItemSerializer(order_items,many=True)
            return Response(serialized_order_items.data,status.HTTP_200_OK)
        return Response(serialized_order_items.errors ,status.HTTP_403_FORBIDDEN)
    
    def put(self,request,id):
        if request.user.groups.filter(name="Manager").exists():

            order = get_object_or_404(Order,id=id)
            serialized_order = OrderSerializer(order,data=request.data)
            if serialized_order.is_valid():
                serialized_order.save()
                return Response(serialized_order.data,status.HTTP_205_RESET_CONTENT)
            return Response(serialized_order.errors,status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_403_FORBIDDEN)



    def patch(self,request,id):
        if request.user.groups.filter(name="Manager").exists():

            order = get_object_or_404(Order,id=id)
            serialized_order = OrderSerializer(order,data=request.data)
            if serialized_order.is_valid():
                serialized_order.save()
                return Response(serialized_order.data,status.HTTP_206_PARTIAL_CONTENT)
            return Response(serialized_order.errors,status.HTTP_400_BAD_REQUEST)


        elif request.user.groups.filter(name="Delivery Crew").exists():
            order = get_object_or_404(Order,id=id)
            
            if order.status == True:
                order.status = False
            else:
                order.status = True

    def delete(self,request,id):
        if request.user.groups.filter(name="Manager").exists():
            order = get_object_or_404(Order,id=id)
            order.delete()
            return Response(status.HTTP_204_NO_CONTENT)
