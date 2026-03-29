from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class Roles(models.Model):
    role_name = models.CharField(max_length=200,unique=True)
    
class Permissions(models.Model):
    permission_name = models.CharField(max_length=200,unique=True)
    
class Module(models.Model):
    module_name = models.CharField(max_length=200,unique=True)
    

class RolePermission(models.Model):
    role = models.ForeignKey(Roles,on_delete=models.PROTECT,null=True,blank=True)
    permission = models.ForeignKey(Permissions,on_delete=models.PROTECT,null=True,blank=True)
    module = models.ForeignKey(Module,on_delete=models.PROTECT,null=True,blank=True)
    
    class Meta:
        unique_together = ['role_id','permission_id','module_id']
    
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role_id = models.ForeignKey(Roles,on_delete=models.PROTECT,null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Subscription(models.Model):
    name = models.CharField(max_length=300)
    max_staff = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    

class Vendor(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    
class Staff(models.Model):
    staff = models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    vendor = models.OneToOneField(Vendor,on_delete=models.PROTECT)
    
    
class Shop(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.PROTECT)
    name = models.CharField(max_length=300)
    gst_number = models.CharField(max_length=13)
    shop_type = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)