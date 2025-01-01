from rest_framework import serializers

from ..authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "address", "staff", "last_login", "active"]
