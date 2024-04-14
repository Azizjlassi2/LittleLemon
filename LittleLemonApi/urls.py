from django.urls import path

from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("menu-items/",MenuItemsView.as_view()),
    path("menu-items/<int:id>/",MenuItemView.as_view()),
    path("groups/manager/users/",ManagerGroupsView.as_view()),
    path("groups/manager/users/<int:id>/",ManagerGroupView.as_view()),
    path("groups/delivery-crew/users/",DeliveryCrewGroupsView.as_view()),
    path("groups/delivery-crew/users/<int:id>",DeliveryCrewGroupView.as_view()),
    path("cart/menu-items/",CartsView.as_view()),
    path("orders/",OrdersView.as_view()),
    path("orders/<int:id>/",OrderView.as_view()),
    path("api-token-auth",obtain_auth_token)
]
