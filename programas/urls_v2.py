from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'programas', ProgramaSerializerViewSet)
router.register(r'tipos-programa', TipoProgramaSerializerViewSet)
router.register(r'objetivos', ObjetivoViewSet, basename='objetivos')

urlpatterns = [
    path('', include(router.urls)),
    path('reporte-programa-pdf/', reporte_programas_pdf, name='reporte-programa-pdf'),
    path('reporte-proyectos-programa/', numero_proyectos_por_programa_pdf, name='reporte-proyectos-programa'),
    path('reporte-preinversion-programa/', numero_preinversion_por_programa_pdf, name='reporte-preinversion-programa'),      
    path('programas/<int:programa_id>/objetivos/', ObjetivoProgramaListView.as_view(), name='objetivo-programa-list'),
    path('programas/<int:programa_id>/objetivos/<int:objetivo_id>/', ObjetivoProgramaDetailView.as_view(), name='objetivo-programa-detail'),
]