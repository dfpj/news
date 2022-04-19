from rest_framework import permissions
from .models import User

def _is_authenticated(request):
    return bool(request.user and request.user.is_authenticated)

def _is_owner_user(request,obj):
    return bool(request.user and request.user.email==obj.email)

def _is_owner_profile(request,obj):
    try:
        user = User.objects.filter(profile_id=obj.id)
        return bool(request.user and request.user==user)
    except User.DoesNotExist:
        return False

def _is_admin(request):
    return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view,obj):
        if not _is_authenticated(request):
            return False
        return  _is_owner_user(request,obj) or _is_admin(request)


class IsOwnerProfileOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view,obj):
        if not _is_authenticated(request):
            return False
        return _is_owner_profile(request, obj) or _is_admin(request)