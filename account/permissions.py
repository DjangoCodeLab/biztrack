from rest_framework.permissions import BasePermission
from account.models import RolePermission

class HasModulePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        
        if not user.is_authenticated:
            return False
        
        if user.role_id and user.role_id.role_name == 'Admin':
            return True
        
        module_name = getattr(view,'module_name',None)
        
        action_map = {
            'list':'read',
            'retrieve':'read',
            'create':'create',
            'update':'update',
            'partial_update':'update',
            'destroy':'delete'
        }
        
        action = action_map.get(view.action)
        
        if not module_name or not action:
            return False 
        return RolePermission.objects.filter(
            role = user.role_id,
            module__module_name = module_name,
            permission__permission_name = action
        ).exists()