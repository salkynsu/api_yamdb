from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.role == "user"


class AdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ("admin", "moderator") or obj.author == request.user


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == "admin"
        )


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == "admin" or request.user.is_superuser)
