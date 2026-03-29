from django.urls import path,include
from account.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'roles',RoleView)
router.register(r'permissions',PermissionView)
router.register(r'modules',ModuleView)
router.register(r'role-permissions',RolePermissionView)
router.register(r'account',AuthViewSet)

urlpatterns = [
    path('',include(router.urls))
]

