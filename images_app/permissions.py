from rest_framework import permissions
from .models import UserProfile, Plan


class CanUploadFile(permissions.BasePermission):
    message = 'You do not have permission to upload files.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user_plan = UserProfile.objects.get(user=request.user).plan
            available_plans = Plan.objects.all()
            if user_plan in available_plans:
                return True
        return False