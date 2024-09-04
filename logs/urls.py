from django.urls import path, include
from .views import UserActionsViewSet


urlpatterns = [
    path('logs/',UserActionsViewSet.as_view(),name="logs")
]