from django.urls import path, include
from .views import LoginView, MeAPI,ListTokensView,DeleteTokenView
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='api.login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('me/', MeAPI.as_view(), name='api.me'),
    path('tokens/', ListTokensView.as_view(), name='list_tokens'),
    path('tokens/delete/', DeleteTokenView.as_view(), name='delete_token')
]

