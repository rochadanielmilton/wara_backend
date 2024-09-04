from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramaSerializerViewSet

router = DefaultRouter()

# router.register(r'programas', Programa2SerializerViewSet)

urlpatterns = [
    # path('', include(router.urls)),
]