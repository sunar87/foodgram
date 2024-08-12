from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
        )
