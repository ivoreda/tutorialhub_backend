from django.contrib.auth import get_user_model
from rest_framework import permissions
from users.models import Tutor  # Make sure to import your Tutor model correctly


class IsTutor(permissions.BasePermission):
    """
    Custom permission to only allow tutors to perform certain actions.
    """

    def has_permission(self, request, view):
        # Check if the request.user is a Tutor
        return Tutor.objects.filter(user=request.user).exists()

class IsAdmin(permissions.BasePermission):
    """
    Custom permissions to only allow tutorialhub admin to perform certain actions.
    """

    def has_permission(self, request, view):
        return request.user.user_type == "Admin"
