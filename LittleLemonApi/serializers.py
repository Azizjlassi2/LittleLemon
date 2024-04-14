from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.MenuItem
        fields = "__all__"


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"username","email"]