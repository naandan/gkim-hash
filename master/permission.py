from rest_framework import permissions


class HasGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        group_permission = view.required_group_permission

        if not request.user.is_authenticated:
            return False
        
        user_permissions = request.user.get_all_permissions()
        return any(perm in group_permission for perm in user_permissions)