from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny


class IsOwnerProfile(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class Allow(AllowAny):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
        )
