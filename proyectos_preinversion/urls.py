from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*
router = DefaultRouter()
router.register(r'tipos-proyecto-preinversion', TiposProyectoPreinversionViewSet)
router.register(r'estados-preinversion', EstadosPreinversionViewSet)
router.register(r'comunidades', ComunidadesViewSet)
router.register(r'preinversion-comunidad', PreinversionComunidadViewSet)
router.register(r'preinversion-organismo-financiador', PreinversionOrganismoFinanciadorViewSet)
router.register(r'proyectos-preinversion', ProyectosPreinversionViewSet)
router.register(r'metas', MetaViewSet, basename='metas')

urlpatterns = [
    path('', include(router.urls)),
    path('proyectos-preinversion/<int:preinversion_id>/metas/', MetaPreinversionListView.as_view(), name='meta-proyectos-preinversion-list'),
    path('proyectos-preinversion/<int:preinversion_id>/metas/<int:meta_id>/', MetaPreinversionDetailView.as_view(), name='meta-proyectos-preinversion-detail'),
]
