from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet  
from rest_framework.response import Response
from account.serializers import *
from account.models import Roles
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework import status
from collections import defaultdict
# Create your views here.


class RoleView(ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializers
    
    
class PermissionView(ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializers
    
    
class ModuleView(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModulesSerializers
    

class RolePermissionView(ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializers
    
    
class AuthViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializers
    
    @action(detail=False,methods=["post"])
    def register(self,request):
        data = request.data
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message":"User Created Successfully!",
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        })
        
        
    @action(detail=False,methods=["post"])
    def login(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = authenticate(request,email=email,password=password)
        
        if user is None:
            return Response({"message":"Invalid Creadentials!"},status=400)
        print("uesr-------------",user)
        user = self.queryset.get(email = user)
        print("user.email,role,------------",user.role_id)
        role = Roles.objects.get(id = user.role_id.pk)
        # ''' "permissions": [
        #     {
        #     "module": "Products",
        #     "actions": ["create", "read", "update", "delete"]
        #     },
        #     {
        #     "module": "Orders",
        #     "actions": ["read", "update"]
        #     }
        # ]'''
        
        role_permission = RolePermission.objects.filter(role_id = user.role_id.pk).select_related('module','permission') 
        permissions_map = defaultdict(list)
        for rt in role_permission:
            module_name = rt.module.module_name
            permission_name = rt.permission.permission_name
            permissions_map[module_name].append(permission_name)

        permission = [
            {
                'module':module,
                'action':action
            } for module,action in permissions_map.items()
        ]
        print("permission--------------------------",permission)
            
                
                
                
        refresh = RefreshToken.for_user(user)
        return Response({
            "message":"Login create Successfully",
            "access":str(refresh.access_token),
            "refresh":str(refresh),
            "Role":user.role_id.role_name,
            "permissions":permission
        })