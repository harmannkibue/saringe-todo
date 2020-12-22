from rest_framework.permissions import BasePermission
SAFE = ["OPTIONS", "POST", "HEAD"]


class IsAuthenticatedOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE or request.user.is_authenticated:
            # print("The authentication is", request.user.is_authenticated)
            return True
        return False


class IsAdminUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.role == "A":
            return True
        return False
