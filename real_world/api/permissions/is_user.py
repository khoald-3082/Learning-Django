from rest_framework import permissions

class IsUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return not user.is_staff
