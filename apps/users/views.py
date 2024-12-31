from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser

from .serializers import UserSerializer

from ..authentication.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'put', 'delete']

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()
