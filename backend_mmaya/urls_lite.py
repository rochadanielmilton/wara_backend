from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_lite import*

router = DefaultRouter()
router.register(r'agencias-financiadoras_select',AgenciaFinanciadoraViewSet, basename='agencias-financiadoras_select')
router.register(r'cargos_select',CargoViewSet, basename='cargos_select')
router.register(r'co-ejecutores_select',CoEjecutorViewSet, basename='co-ejecutor_select')
router.register(r'departamentos_select',DepartamentoViewSet, basename='departamentos_select')
router.register(r'descentralizadas_select',DescentralizadaViewSet, basename='descentralizadas_select')
router.register(r'ejecutores_select',EjecutorViewSet, basename='ejecutores_select')
router.register(r'empresa-constructora_select',EmpresaConstructoraViewSet, basename='empresa-constructora_select')
router.register(r'estados_select',EstadoViewSet, basename='estados_select')
router.register(r'estados-detallados_select', EstadoDetalladoViewSet, basename='estados-detallados_select')
router.register(r'lugares_select',LugarViewSet, basename='lugares_select')
router.register(r'ministerios_select',MinisterioViewSet, basename='ministerios_select')
router.register(r'municipios_select',MunicipioViewSet, basename='municipios_select')
router.register(r'organizaciones-financieras_select',OrganizacionFinancieraViewSet, basename='organizaciones-financieras_select')
router.register(r'provincias_select',ProvinciaViewSet, basename='provincias')
router.register(r'responsables-contraparte_select',ResponsableContraparteViewSet, basename='responsables-contraparte_select')
router.register(r'sectores_select',SectorViewSet, basename='sectors_select')
router.register(r'tipos-financiamiento_select',TipoFinanciamientoViewSet, basename='tipos-financiamiento_select')
router.register(r'tipos-proyecto_select',TipoProyectoViewSet, basename='tipos-proyecto_select')
router.register(r'ucep-responsables_select',UcepResponsableViewSet, basename='ucep-responsable_select')
router.register(r'viceministerios_select',ViceministerioViewSet, basename='viceministerios_select')
router.register(r'programas_select',ProgramasViewSet, basename='programas_select')
router.register(r'proyectos-preinversion_select',ProyectosPreinversionViewSet, basename='proyectos-preinversion_select')



urlpatterns = [
    path('sector-detallado/<int:pk>/',SectorDetalleViewSet.as_view(), name='sector-detalle'),
    path('', include(router.urls))
]

urlpatterns += router.urls  
