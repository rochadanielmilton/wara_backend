from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'permissions', AuthPermissionViewSet,basename='permissions')
router.register(r'groups',AuthGroupViewSet, basename='groups')
router.register(r'content-type',ContentTypeView, basename='content-type')
router.register(r'permissions-user',AuthUserUserPermissionsViewSet, basename='permission-user')
router.register(r'permissions-group',AuthGroupPermissionsViewSet, basename='permissions-group')
router.register(r'users-group',AuthUserGroupsViewSet,basename='users-group')
router.register(r'menus-user',UserMenuViewSet,basename='menus-user')
router.register(r'menu-group',GroupMenuViewSet,basename='menu-group')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('sector/users/', SectorUserListCreateView.as_view(), name='sector-user-list-create'),
    path('sector/users/<int:pk>/', SectorUserRetrieveUpdateDestroyView.as_view(), name='sector-user-detail'),
]