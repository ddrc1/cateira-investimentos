from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated.has_permission(self, request, view) and request.method in SAFE_METHODS
