from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .password_validation import validators

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_password(self, value):
        try:
            validate_password(value, validators)
        except ValidationError as e:
            raise serializers.ValidationError(f"Error in setting password: {str(e)}")
        return value
    
    def create(self, validated_data):
        User.objects.create_user(**validated_data)
        return validated_data
    

class TokensSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        
        if not user.active:
            raise AuthenticationFailed('Deactivated user')

        return user
    
    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'tokens': TokensSerializer(instance.tokens()).data
        }

        return representation
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
