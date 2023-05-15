from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'