from rest_framework import permissions

class AdminPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            if (request.user.studentinfo.power>=1):
                return True
            else:
                return False
        except AttributeError:
            return False
#Todo:对象权限