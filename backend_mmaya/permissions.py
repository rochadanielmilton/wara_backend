from rest_framework import permissions

class IsSectorUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_sector()

class IsInGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        required_groups = getattr(view, 'required_groups', [])

        if request.user.is_authenticated:
            if request.user.groups.filter(name__in=required_groups).exists():
                return True

        return False