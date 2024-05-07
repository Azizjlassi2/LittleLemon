from django.urls import path

from .views import *

urlpatterns = [
    # Menu-Item
    path("menu-items/",MenuItemsView.as_view(),name="menu-items"),
    path("menu-items/<int:id>/",MenuItemView.as_view(),name="single-menu-item"),

    #Categories
    path("categories/",CategoriesView.as_view(),name="categories"),
    path("categories/<int:id>/",CategoryView.as_view(),name="single-category"),

    # Manager Members
    path("manager/users/",ManagerGroupsView.as_view(),name="managers"),
    path("manager/users/<int:id>/",ManagerGroupView.as_view(),name="single-manager"),

    # Delivery Crew Members
    path("delivery-crew/users/",DeliveryCrewGroupsView.as_view(),name="delivery-crews"),
    path("delivery-crew/users/<int:id>/",DeliveryCrewGroupView.as_view(),name="single-delivery-crew"),

    # Cart
    path("carts/menu-items/",CartsView.as_view(),name="carts"),

    # Orders
    path("orders/",OrdersView.as_view(),name="orders"),
    path("orders/<int:id>/",OrderView.as_view(),name="single-order"),

]
