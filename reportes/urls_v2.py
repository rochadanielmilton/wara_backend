
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'lista-proyectos',ListaProyectosView, basename='lista-proyectos')

urlpatterns = [
    path('list-proyectos-por-municipio/', ListProyectosPorProvinciaView.as_view(), name='lista-proyectos-por-municipio'),
    path('programas-proyectos-inversion-por-depto-prov-mun/', 
            ProgramasProyectosInversionPorDeptoProvMunView.as_view(), 
            name='programas-proyectos-inversion-por-depto-prov-mun'
    ),
    path('por-gestion/',ProyectoPorGestionView.as_view(), name='proyectos-por-gestion'),
    path('data-por-sectores/',datosPorSectoresView.as_view(), name='data-por-sectores'),
    path('inversion-por-gobierno/',InversionPorGobiernoView.as_view(), name='inversion-por-gobierno'),
    path('total-inver-porcentajes/',TotalInversionPorcentajes.as_view(), name='total-inver-porcentajes'),    
    path('proyectos-por-municipio-pdf/', proyecto_por_municipio_pdf, name='proyecto-por-municipio-pdf'),
    path('proyectos-por-municipio-excel/', proyecto_por_municipio_excel, name='proyectos-por-municipio-excel'),
    path('reporte_general_pdf/', reporte_general_pdf, name='reporte_general_pdf'),
    path('proyectos-por-busqueda/',proyectos_por_busqueda_pdf, name = 'proyectos-por-busqueda'), 
    path('reporte-general-por-sector/',reporte_por_sector_y_estado_pdf, name='reporte-general-por-sector'),   
]