from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Check if the request user is the owner of the object."""
    def has_object_permission(self, request, view, obj):
        return True if request.method in permissions.SAFE_METHODS else obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """The request is user an admin, or is a read-only request."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
