from rest_framework.permissions import BasePermission

MANAGE_ROLES = ("teacher", "admin")


class CanManageQuestions(BasePermission):
    """Teacher or admin/board operator can author and manage questions."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_staff or (getattr(user, "role", None) in MANAGE_ROLES)