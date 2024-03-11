from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.is_admin())
                or request.method in permissions.SAFE_METHODS)


class IsModeratorIsAdminIsAuthorOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                and (
                    request.user.is_moderator()
                    or request.user.is_admin()
                    or (obj.author == request.user)
                ))
                or request.method in permissions.SAFE_METHODS)

class IsOwnerOrIsAdmin(permissions.IsAdminUser):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin()
                     or request.user.is_superuser)
                )

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                 and (request.user.is_admin()
                      or request.user.is_superuser))
                or obj.author == request.user)