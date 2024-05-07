from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group
from django.core.paginator import Paginator , EmptyPage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


from .serializers import *
from .models import *







class MenuItemsView(APIView):
    
    permission_classes = [ IsAuthenticated ]    

   
    # Caching
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request) -> Response:

        """

        Return `MenuItem` list 

        ### Filtering

        - `category`
        - `price`
        - `featured`

        ### Searching

        - `search` : search by `title`

        """
        # Query
        items = MenuItem.objects.all().order_by("title")

        # Filtering 
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        featured_option = request.query_params.get('featured')

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if featured_option:
            items = items.filter(featured=featured_option)

        # Searching
        search = request.query_params.get('search') #search by title
        if search:
            items = items.filter(title__icontains=search)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            items.order_by(*ordering_fields)

        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)


        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []


        # Serialization
        serialized_items = MenuItemSerializer(items,many=True)
        return Response(serialized_items.data,status.HTTP_200_OK)

    def post(self,request) -> Response:
        """

        Only `Manager` group users can have access

        """
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

    def get(self,request,id) -> Response:
        item = get_object_or_404(MenuItem,pk = id)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data,status.HTTP_200_OK)

    def put(self,request,id) -> Response:
        
        if request.user.groups.filter(name="Manager").exists():
            item = get_object_or_404(MenuItem,pk = id)
            serialized_item = MenuItemSerializer(item,data=request.data)
            if serialized_item.is_valid():
                serialized_item.save()
                return Response(serialized_item.data,status=status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_item.data,status=status.HTTP_304_NOT_MODIFIED)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id) -> Response:

        if request.user.groups.filter(name="Manager").exists():
            item = get_object_or_404(MenuItem,pk = id)
            message = f"MenuItem {item.id} : {item.title} deleted !"
            item.delete()
            return Response(message,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
class ManagerGroupsView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    # Caching
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request):
        #Suery
        users = User.objects.filter(groups__name__in =["Manager"]).order_by("username")
        
        # Filtering
        date_joined  = request.query_params.get('joined')
        if date_joined:
            users = users.filter(date_joined__lte=date_joined)
            
        # Searching
        search = request.query_params.get('search')
        if search:
            users = users.filter(username__icontains=search)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            users.order_by(*ordering_fields)

        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)

        paginator = Paginator(users,per_page=perpage)
        try:
            users = paginator.page(number=page)
        except EmptyPage:
            users = []


        serialized_users = UserManagerGroupSerializer(users,many=True)
        return Response(serialized_users.data,status.HTTP_200_OK)
    

    def post(self,request):
        if request.user.groups.filter(name="Manager").exists():
            
            serialized_user = UserManagerGroupSerializer(data=request.data)
            if serialized_user.is_valid():
                serialized_user.save()
                
                manager_group  = Group.objects.get(name="Manager")
                user = User.objects.get(pk=serialized_user.data.get("id"))
                user.groups.add(manager_group)
                user.save()


                data = serialized_user.data
                data["groups"] = GroupSerializer(manager_group).data
                
                return Response(data,status.HTTP_201_CREATED)
            else:
                return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status.HTTP_403_FORBIDDEN)

class ManagerGroupView(APIView):
    
    permission_classes = [IsAuthenticated]


    def get(self,request,id) -> Response:
        user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
        
        serialized_user = UserManagerGroupSerializer(user)
        return Response(serialized_user.data,status.HTTP_200_OK)

    def put(self,request,id) -> Response:
        
        if request.user.groups.filter(name="Manager").exists():
            
            user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
            print(user)
            serialized_user = UserManagerGroupSerializer(user,data=request.data)
            print(serialized_user)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_user.data,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id) -> Response:

        if request.user.groups.filter(name="Manager").exists():
            user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
            message = f"Manager Member {user.id} : {user.username} deleted !"
            user.delete()
            try:
                user = get_object_or_404(User,pk = id,groups__name__in =["Manager"])
            except Exception:
                return Response(status.HTTP_404_NOT_FOUND)
            return Response(message,status.HTTP_200_OK)
        return Response(status.HTTP_403_FORBIDDEN)
    
class DeliveryCrewGroupsView(APIView):
    
    permission_classes = [IsAuthenticated]

    # Caching
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request) -> Response:
        users = User.objects.filter(groups__name__in =["Delivery Crew"]).order_by("username")
         
        # Filtering
        date_joined  = request.query_params.get('joined')
        if date_joined:
            users = users.filter(date_joined__lte=date_joined)
            
        # Searching
        search = request.query_params.get('search')
        if search:
            users = users.filter(username__icontains=search)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            users.order_by(*ordering_fields)

        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)

        paginator = Paginator(users,per_page=perpage)
        try:
            users = paginator.page(number=page)
        except EmptyPage:
            users = []
        serialized_users = UserDeliveryGroupSerializer(users,many=True)
        return Response(serialized_users.data,status.HTTP_200_OK)
    

    def post(self,request) -> Response:
        if request.user.groups.filter(name="Manager").exists():

            serialized_user = UserDeliveryGroupSerializer(data=request.data)
            if serialized_user.is_valid():
                serialized_user.save()

                delivery_group  = Group.objects.get(name="Delivery Crew")
                user = User.objects.get(pk=serialized_user.data.get("id"))
                user.groups.add(delivery_group)
                user.save()


                data = serialized_user.data
                data["groups"] = GroupSerializer(delivery_group).data
                
                return Response(data,status.HTTP_201_CREATED)
            else:
                return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status.HTTP_403_FORBIDDEN)

class DeliveryCrewGroupView(APIView):
    
    permission_classes = [IsAuthenticated]


    def get(self,request,id) -> Response:
        user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
        
        serialized_user = UserDeliveryGroupSerializer(user)
        return Response(serialized_user.data,status.HTTP_200_OK)

    def put(self,request,id) -> Response:
        
        if request.user.groups.filter(name="Manager").exists():
            user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
            serialized_user = UserDeliveryGroupSerializer(user,data=request.data)
            if serialized_user.is_valid():
                serialized_user.save()
                return Response(serialized_user.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_user.errors,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id) -> Response:

        if request.user.groups.filter(name="Manager").exists():
            user = get_object_or_404(User,pk = id,groups__name__in =["Delivery Crew"])
            message = f"Delivery Crew Member {user.id} : {user.username} deleted !"
            user.delete()
            return Response(message,status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_403_FORBIDDEN)
    
class CartsView(APIView):

    permission_classes = [IsAuthenticated]

    # Caching
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request) -> Response:
       
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

        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)


        paginator = Paginator(carts,per_page=perpage)
        try:
            carts = paginator.page(number=page)
        except EmptyPage:
            carts = []

        serialized_carts = CartSerializer(carts,many=True)
        return Response(serialized_carts.data,status.HTTP_200_OK)
    
    def post(self,request) -> Response:
      
        data = request.data.copy()
        data["user"] = f"{request.user.id}"
        
        
        serialized_cart = CartSerializer(data=data)
        print(serialized_cart)
        if serialized_cart.is_valid():
            serialized_cart.save()
            
            return Response(serialized_cart.data,status.HTTP_201_CREATED)
        else:
            return Response(serialized_cart.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request) -> Response:
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

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            orders.order_by(*ordering_fields)
        
     
        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)


        paginator = Paginator(orders,per_page=perpage)
        try:
            orders = paginator.page(number=page)
        except EmptyPage:
            orders = []

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

    def get(self,request,id) -> Response:


        order = get_object_or_404(Order,id=id)
        order_items = OrderItem.objects.filter(order=order)
        if order.user.pk == request.user.id:
            serialized_order_items = OrderItemSerializer(order_items,many=True)
            return Response(serialized_order_items.data,status.HTTP_200_OK)
        return Response(serialized_order_items.errors ,status.HTTP_403_FORBIDDEN)
    
    def put(self,request,id) -> Response:
        if request.user.groups.filter(name="Manager").exists():

            order = get_object_or_404(Order,id=id)
            serialized_order = OrderSerializer(order,data=request.data)
            if serialized_order.is_valid():
                serialized_order.save()
                return Response(serialized_order.data,status.HTTP_205_RESET_CONTENT)
            return Response(serialized_order.errors,status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_403_FORBIDDEN)



    def patch(self,request,id) -> Response:
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

    def delete(self,request,id) -> Response:
        if request.user.groups.filter(name="Manager").exists():
            order = get_object_or_404(Order,id=id)
            order.delete()
            return Response(status.HTTP_204_NO_CONTENT)

class CategoriesView(APIView):

    permission_classes = [ IsAuthenticated ]    

   

   # Caching
    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request) -> Response:


        
        # Query
        categories = Category.objects.all().order_by("title")

        # Filtering 
        category_name = request.query_params.get('category')
        

        if category_name:
            categories = categories.filter(category__title=category_name)
        
        # Searching
        search = request.query_params.get('search') #search by title
        if search:
            categories = categories.filter(title__icontains=search)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            categories.order_by(ordering)

        # Pagination
        perpage = request.query_params.get('perpage',default=8)
        page = request.query_params.get('page',default=1)


        paginator = Paginator(categories,per_page=perpage)
        try:
            categories = paginator.page(number=page)
        except EmptyPage:
            categories = []


        # Serialization
        serialized_categories = CategorySerializer(categories,many=True)
        return Response(serialized_categories.data,status.HTTP_200_OK)


    def post(self,request) -> Response:
        """

        Only `Manager` group users can have access

        """
        if request.user.groups.filter(name="Manager").exists():
            serialzed_category = CategorySerializer(data=request.data)
            if serialzed_category.is_valid():
                serialzed_category.save()
                return Response(serialzed_category.data,status.HTTP_201_CREATED)
            else:
                return Response(serialzed_category.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_403_FORBIDDEN)
    
class CategoryView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request,id) -> Response:
        category = get_object_or_404(Category,pk = id)
        serialized_category= CategorySerializer(category)
        return Response(serialized_category.data,status.HTTP_200_OK)

    def put(self,request,id) -> Response:
        
        if request.user.groups.filter(name="Manager").exists():
            category = get_object_or_404(Category,pk = id)
            serialized_category = CategorySerializer(category,data=request.data)
            if serialized_category.is_valid():
                serialized_category.save()
                return Response(serialized_category.data,status.HTTP_206_PARTIAL_CONTENT)
            
            return Response(serialized_category.data,status.HTTP_304_NOT_MODIFIED)
        return Response(status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,id) -> Response:

        if request.user.groups.filter(name="Manager").exists():
            category = get_object_or_404(Category,pk = id)
            message = f"Category {category.id} : {category.title} deleted !"
            category.delete()
            return Response(message,status.HTTP_200_OK)
        return Response(status.HTTP_403_FORBIDDEN)
    
       


