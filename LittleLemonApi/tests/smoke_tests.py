from django.test import TestCase,Client 
from rest_framework.test import force_authenticate ,APIRequestFactory
from rest_framework.views import  APIView
from django.contrib.auth.models import User , Group
from rest_framework import status
from ..views import *
from django.urls import reverse


# py manage.py test LittleLemonApi.tests.smoke_tests
class SmokeTest(TestCase):

    def setUp(self) -> None:
        self.client = APIRequestFactory()
        self.user = User.objects.create(
            username="chipy",
        )
        self.managers_group = Group.objects.create(
            name="Manager"
        )
        self.delivery_crew_groups = Group.objects.create(
            name="Delivery Crew"
        )
        self.view : APIView 

    def test__menu_items_endpoint(self):

        # SETUP
        self.view = MenuItemsView.as_view()
        category_item = Category.objects.create(
            title="category_title_1",
            slug="category_slug_1",
        )
        body = {
            "title"     : "menu_item_1",
            "price"     : 21.0,
            "stock"     : 100,
            "featured"  : True,
            "category_id"  :  category_item.pk,

        }

        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get(path=reverse("menu-items"))
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request)

        #SETUP
        self.user.groups.add(self.managers_group)

        # POST REQUEST
        post_request = self.client.post(path=reverse("menu-items"),data=body)
        force_authenticate(post_request,self.user)
        post_response = self.view(post_request)
        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(post_response.status_code,201)
    
    def test_single_menu_item_endpoint(self):

        # SETUP
        self.view = MenuItemView.as_view()
        category_item = Category.objects.create(
            title="category_title_1",
            slug="category_slug_1",
        )
        menu_item = MenuItem.objects.create(
            title="menu_item_1",
            price=21.0,
            stock = 100,
            featured = True,
            category = category_item


            )
        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get("/menu-items/")
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request,id=menu_item.pk)

        #SETUP
        self.user.groups.add(self.managers_group)

        # PUT REQUEST
        put_request = self.client.get("/menu-items/",data={"stock":200})
        force_authenticate(put_request,self.user)
        put_response = self.view(put_request,id=menu_item.pk)


        # DELETE REQUEST
        delete_request = self.client.get("/menu-items/")
        force_authenticate(delete_request,self.user)
        delete_response = self.view(delete_request,id=menu_item.pk)


        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(put_response.status_code ,200)
        self.assertEqual(delete_response.status_code,200)

    def test_managers_endpoint(self):
    

        # SETUP
        self.view = ManagerGroupsView.as_view()
        self.user.groups.add(self.managers_group)
        body = {
            "username":"manager_username",
            "email":"manager_email@gmail.com",
            "password": "manager_username_password"
           
        }

        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get(path=reverse("managers"))
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request)

        # POST REQUEST
        post_request = self.client.post(path="/groups/manager/users/",data=body)
        force_authenticate(post_request,self.user)
        post_response = self.view(post_request)

        

        id = post_response.data.get("id")
        user = User.objects.get(pk=id)
        manager_group = user.groups.filter(name="Manager").exists()
        
        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(post_response.status_code,201)
        self.assertTrue(manager_group)

    def test_single_manager_endpoint(self):

        # SETUP
        self.view = ManagerGroupView.as_view()
        self.user.groups.add(self.managers_group)
       
        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get("/groups/manager/users/<int:id>/")
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request,id=self.user.pk)


        # PUT REQUEST
        put_request = self.client.get("/groups/manager/users/<int:id>/",data={"username":"new_manager_username"})
        force_authenticate(put_request,self.user)
        put_response = self.view(put_request,id=self.user.pk)


        # DELETE REQUEST
        delete_request = self.client.get("/groups/manager/users/<int:id>/")
        force_authenticate(delete_request,self.user)
        delete_response = self.view(delete_request,id=self.user.pk)


        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(put_response.status_code ,200)
        self.assertEqual(delete_response.status_code,200)

    def test_categories_endpoint(self):
        

            # SETUP
            self.view = CategoriesView.as_view()
            self.user.groups.add(self.managers_group)
            body = {
                "title": "category_title_1",
                "slug":"category_slug_1",
            }

            
            # TEST CASES

            # GET REQUEST
            get_request = self.client.get(path=reverse("categories"))
            force_authenticate(get_request,self.user)
            get_response = self.view(get_request)

            # POST REQUEST
            post_request = self.client.post(path="/categories/",data=body)
            force_authenticate(post_request,self.user)
            post_response = self.view(post_request)
            
            
            #CHECK
            self.assertEqual(get_response.status_code,200)
            self.assertEqual(post_response.status_code,201)

    def test_single_category_endpoint(self):

        # SETUP
        self.view = ManagerGroupView.as_view()
        self.user.groups.add(self.managers_group)
        
        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get("/categories/<int:id>/")
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request,id=self.user.pk)


        # PUT REQUEST
        put_request = self.client.get("/categories/<int:id>/",data={"title":"new_title"})
        force_authenticate(put_request,self.user)
        put_response = self.view(put_request,id=self.user.pk)


        # DELETE REQUEST
        delete_request = self.client.get("/categories/<int:id>/")
        force_authenticate(delete_request,self.user)
        delete_response = self.view(delete_request,id=self.user.pk)


        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(put_response.status_code ,200)
        self.assertEqual(delete_response.status_code,200)

    def test_delivery_crew_endpoint(self):
    

        # SETUP
        self.view = DeliveryCrewGroupsView.as_view()
        self.user.groups.add(self.managers_group)
        body = {
            "username":"delivery_crew_username",
            "email":"delivery_crew_email@gmail.com",
            "password": "delivery_crew_username_password"
           
        }

        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get(path=reverse("delivery-crews"))
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request)

        # POST REQUEST
        post_request = self.client.post(path="/groups/delivery-crew/users/",data=body)
        force_authenticate(post_request,self.user)
        post_response = self.view(post_request)


        id = post_response.data.get("id")
        user = User.objects.get(pk=id)
        delivery_group = user.groups.filter(name="Delivery Crew").exists()
        
        
        
        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(post_response.status_code,201)
        self.assertTrue(delivery_group)
"""
    def test_single_delivery_crew_endpoint(self):

        # SETUP
        self.view = ManagerGroupView.as_view()
        self.user.groups.add(self.managers_group)
       
        
        # TEST CASES

        # GET REQUEST
        get_request = self.client.get("/groups/manager/users/<int:id>/")
        force_authenticate(get_request,self.user)
        get_response = self.view(get_request,id=self.user.pk)


        # PUT REQUEST
        put_request = self.client.get("/groups/manager/users/<int:id>/",data={"username":"new_manager_username"})
        force_authenticate(put_request,self.user)
        put_response = self.view(put_request,id=self.user.pk)


        # DELETE REQUEST
        delete_request = self.client.get("/groups/manager/users/<int:id>/")
        force_authenticate(delete_request,self.user)
        delete_response = self.view(delete_request,id=self.user.pk)


        
        #CHECK
        self.assertEqual(get_response.status_code,200)
        self.assertEqual(put_response.status_code ,200)
        self.assertEqual(delete_response.status_code,200)
"""
    