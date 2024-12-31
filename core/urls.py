"""
URL configuration for carteira_investimentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

router = routers.DefaultRouter()

# Swagger schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Carteira de Investimentos",
      default_version='v1',
      description="API de carteira de investimentos customizada",
      terms_of_service=None,
      contact=openapi.Contact(email="danielrotheia@gmail.com"),
      license=None,
   ),
   permission_classes=(AllowAny,),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include((router.urls, 'api'), namespace='api')),
    path(r'api/stocks/', include(('apps.stocks.urls', 'apps.stocks'), namespace='stocks')),
    path(r'api/operations/', include(('apps.operations.urls', 'apps.operations'), namespace='operations')),
    path(r'api/accounts/', include(('apps.authentication.urls', 'apps.authentication'), namespace='authentication')),
    path(r'api/users/', include(('apps.users.urls', 'apps.users'), namespace='users')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
]
