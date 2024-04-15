from django.test import TestCase
from rest_framework.test import APIRequestFactory,force_authenticate
from django.contrib.auth.models import User


# Create your tests here.


# Users Groups
manager = User.objects.get(username='admin') # Manager Group
delivery = User.objects.get(username='delivery1') # Delivery Crew Group


factory = APIRequestFactory()

# MenuItemView Tests

