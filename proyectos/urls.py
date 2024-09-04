from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
#router.register(r'proyectos', ProyectosViewSet)
router.register(r'realizaciones', RealizacionesViewSet,basename='realizaciones')
router.register(r'seguimientos',SeguimientoViewSet,basename='seguimiento')
router.register(r'seguimientos-admin',SeguimientoAdminViewSet,basename='seguimiento-admin')
router.register(r'proyectos',ProyectosViewSet, basename='proyecto')
router.register(r'agua-saneamiento/proyectos',AguaSaneamientoProyectoViewSet, basename='agua-saneamiento-proyectos')
router.register(r'cuencas/proyectos',CuencasProyectoViewSet, basename='cuencas-proyectos')
router.register(r'residuos/proyectos',ResiduosProyectoViewSet, basename='residuos-proyectos')
router.register(r'riego/proyectos',RiegoProyectoViewSet, basename='riego-proyectos')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'proyectos/<int:proyecto_id>/conexiones/',
        ConexionesViewSet.as_view(),
        name='conexiones'),
    path(
        'proyectos/<int:proyecto_id>/drenajes-pluviales/',
        DrenajesPluvialesViewSet.as_view(),
        name='drenajes-pluviales'),
    path(
        'proyectos/<int:proyecto_id>/poblaciones/',
        PoblacionesViewSet.as_view(),
        name='poblaciones'),   
    path(
        'proyectos/<int:proyecto_id>/variables-impacto/',
        VariablesImpactoViewSet.as_view(),
        name='variables-impacto'),
    
    path('reporte-ficha-tecnica-pdf/', reporte_ficha_tecnica_pdf, name='reporte-ficha-tecnica-pdf'),
    path('reporte_avance_proyecto_pdf/', reporte_avance_proyecto_pdf, name='reporte_avance_proyecto_pdf'),    
    path('reporte-seguimiento-mensual-pdf/',reporte_seguimiento_mensual_pdf, name='reporte-seguimiento-mensual-pdf'),
    path('obtener-ficha-tecnica/',obtenerFichaTecnicaView.as_view(), name='obtener-ficha-tecnica'),
    path('update-geo-localizacion/',actualizarGeorreferenciacionAPIView.as_view(), name='update-geo-localizacion'),
    path('baja-ultimo-seguimiento/',bajaSeguimientoEspecificoAPIView.as_view(), name='baja-ultimo-seguimiento'),
    path('aprobacion-seguimiento/',aprobacionSeguimientoAPIView.as_view(), name='aprobacion-seguimiento'),
    path('actualizar-indicadores/',UpdateIndicadoresAPIView.as_view(), name='actualizar-indicadores'),
    path('revision-seguimiento/<int:pk>/', SeguimientoParaValidacionView.as_view(), name='revision-seguimiento'),
    path('rechazar-seguimiento/', rechazarSeguimientoAPIView.as_view(), name='rechazar-seguimiento'),
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)