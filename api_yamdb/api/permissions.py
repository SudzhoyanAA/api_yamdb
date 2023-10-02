from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser
        )
        )
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser)


class IsYourself(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if reverse('users-me') in request.build_absolute_uri():
            if request.method in ['GET', 'DELETE']:
                return True
            elif request.method == 'PATCH':
                if 'role' not in request.data:
                    return True
        return False


class IsUser(permissions.BasePermission):
    """Кастомный класс для проверки прав для роли user."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'user'
                     or request.user.role == 'admin'
                     or request.user.role == 'moderator'))

    def has_object_permission(self, request, view, obj):
        """Функция проверяет является ли пользователь user."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and obj.author == request.user
                and (request.user.role == 'user'
                     or request.user.role == 'admin'
                     or request.user.role == 'moderator'))
