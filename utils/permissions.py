# Here we will be creating permissions required for the whole project.
from rest_framework import permissions
from HMS.choices import RoleChoices


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        print(f"USER = {request.user}")

        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, "role") and request.user.role == RoleChoices.ADMIN:
            return True

        return False


class IsAppointmentHolderUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(f"REQUESTED USER = {request.user}")
        print(f"OBJECT USER = {obj.user_patient.user}")
        return request.user == obj.user_patient.user


class IsAppointmentHolderDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.doctor.user

class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        print(f"USER = {request.user.id}")

        if not request.user.is_authenticated:
            return False

        if hasattr(request.user, "role") and request.user.role == RoleChoices.STAFF:
            return True

        return False
