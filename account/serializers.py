from rest_framework import serializers
from account.models import *

class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id','role_name']
    

class PermissionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id','permission_name']
        
class ModulesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id','module_name']

class RolePermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id','role','permission','module']
        
class UsersSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confim_password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','email','role_id','password','confim_password']
    
    def validate(self, data):
        if data['confim_password'] != data['password']:
            raise serializers.ValidationError("Confim password and password must match")
        return data 
        
        
    def create(self, validated_data):
        validated_data.pop('confim_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    