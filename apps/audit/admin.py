from django.contrib import admin

from .models import Audit

class AdminAudit(admin.ModelAdmin):
    list_display = ('id', 'table', 'object_id', 'updated_at', 'old_values', 'user')
    list_filter = ('table', 'updated_at', 'user')

admin.site.register(Audit, AdminAudit)
