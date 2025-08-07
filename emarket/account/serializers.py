from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from django.contrib.auth import authenticate
class SingUpSerializer(serializers.ModelSerializer):


      extra_kwargs ={
         'first_name':{'required':True , 'allow_blank': False},
         'last_name':{'required':True , 'allow_blank': False},
         'email' :{'required':True , 'allow_blank': False},
         'password' :{'required':True , 'allow_blank': False , 'min_length':8},
      }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model = User
      fields = ('first_name' , 'last_name','email' , 'username')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        data = super().validate({"username": username, "password": password})

        data["user"] = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return data
    
    
class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'write_only': True, 'min_length': 8},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPoints

class ChargePointsSerializer(serializers.Serializer):
    username = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("المستخدم غير موجود")
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        amount = self.validated_data['amount']
        user_points, _ = UserPoints.objects.get_or_create(user=user)
        user_points.points += amount
        user_points.save()
        return user_points
