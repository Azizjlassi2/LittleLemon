from django.urls import path

from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Menu-Item
    path("menu-items/",MenuItemsView.as_view()),
    path("menu-items/<int:id>/",MenuItemView.as_view()),

    #Categories
    path("categories/",CategoriesView.as_view()),
    path("categories/<int:id>/",CategoryView.as_view()),

    # Manager Members
    path("groups/manager/users/",ManagerGroupsView.as_view()),
    path("groups/manager/users/<int:id>/",ManagerGroupView.as_view()),

    # Delivery Crew Members
    path("groups/delivery-crew/users/",DeliveryCrewGroupsView.as_view()),
    path("groups/delivery-crew/users/<int:id>",DeliveryCrewGroupView.as_view()),

    # Cart
    path("carts/menu-items/",CartsView.as_view()),

    # Orders
    path("orders/",OrdersView.as_view()),
    path("orders/<int:id>/",OrderView.as_view()),

    # Auth Token
    path("api-token-auth",obtain_auth_token)
]
