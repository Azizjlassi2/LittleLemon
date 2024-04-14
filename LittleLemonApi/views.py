from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User , Group
from .models import MenuItem
from .serializers import *
from rest_framework.permissions import IsAuthenticated




class MenuItemsView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request):
        items = MenuItem.objects.all()
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
            return Response(message,status.HTTP_200_OK)
        return Response(status.HTTP_403_FORBIDDEN)
    

