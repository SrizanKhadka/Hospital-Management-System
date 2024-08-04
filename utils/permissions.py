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


class IsAppointmentHolder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(f"REQUESTED USER = {request.user}")
        print(f"OBJECT USER = {obj.user_patient.user}")
        return request.user == obj.user_patient.user
