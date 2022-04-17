from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.role == "admin"
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user == "admin" and request.user.is_staff)
