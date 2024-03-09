from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    # здесь нужно скорее всего поменять проверку роли, когда допилят user
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin()))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin()))
