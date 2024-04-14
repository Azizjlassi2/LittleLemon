from django.urls import path

from .views import *

urlpatterns = [
    path("menu-items/",MenuItemsView.as_view()),
    path("menu-items/<int:id>/",MenuItemView.as_view()),
    path("groups/manager/users/",ManagerGroupsView.as_view()),
    path("groups/manager/users/<int:id>/",ManagerGroupView.as_view()),
    path("groups/delivery-crew/users/",DeliveryCrewGroupsView.as_view()),
    path("groups/delivery-crew/users/<int:id>",DeliveryCrewGroupView.as_view()),
]
