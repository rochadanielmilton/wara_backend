from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthPermissionViewSet, AuthGroupViewSet, UserListCreateView,UserRetrieveUpdateDestroyView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]