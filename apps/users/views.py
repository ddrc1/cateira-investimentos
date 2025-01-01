from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from ..utils.pagination import CustomPageNumberPagination

from .serializers import UserSerializer
from .swagger.swagger_serializers import PaginatedUserResponseSerializer

from ..authentication.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'put', 'delete']
    pagination_class = CustomPageNumberPagination

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()

    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedUserResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
