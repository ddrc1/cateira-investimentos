from rest_framework import serializers

from ..serializers import UserSerializer

class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()


class PaginatedUserResponseSerializer(PaginatedResponseSerializer):
    results = UserSerializer(many=True)
