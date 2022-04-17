from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.role == "admin"
        )
        # return (
        #     request.user.is_authenticated and
        #         (request.user.is_staff or request.user.role == "admin")
        #     or request.method in permissions.SAFE_METHODS
        #     )