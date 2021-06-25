from rest_framework import permissions

class SuperAdminPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        try:            
            if (request.user.studentinfo.power==2):
                return True
            else:
                return False
        except AttributeError:
            return False
class ActivityPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.user==obj.owner.user):
            return True
        else:
            return False
        
class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if (request.user.studentinfo.power>=1):
                return True
            else:
                return False
        except AttributeError:
            return False