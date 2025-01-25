from django.contrib import admin
from ..authentication.models import User

class AdminUser(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'address', 'staff', 'active', 'date_joined', 'last_login')
    list_filter = ('staff', 'active', 'date_joined', 'last_login')
    list_editable = ('email', 'username', 'address', 'staff', 'active')
    search_fields = ['username']
    list_per_page = 20


admin.site.register(User, AdminUser)
