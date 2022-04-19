from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user or request.user.role == "user")


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_staff or request.user.role == "admin")
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == "admin" or request.user.is_superuser)
