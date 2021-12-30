from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SportGame


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportGame
        fields = '__all__'
