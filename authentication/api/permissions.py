# Here we will be creating permissions required for registration.
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print(f"USER = {request.user}")

        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, "role") and request.user.role == "ADMIN":
            return True

        return False
