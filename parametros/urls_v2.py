from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'agencias-financiadoras', views.AgenciaFinanciadoraViewSet, basename='agencias-financiadoras')
router.register(r'cargos', views.CargoViewSet, basename='cargos')
router.register(r'co-ejecutores', views.CoEjecutorViewSet, basename='co-ejecutor')
router.register(r'departamentos', views.DepartamentoViewSet, basename='departamentos')
router.register(r'descentralizadas', views.DescentralizadaViewSet, basename='descentralizadas')
router.register(r'ejecutores', views.EjecutorViewSet, basename='ejecutores')
router.register(r'empresa-constructora', views.EmpresaConstructoraViewSet, basename='empresa-constructora')
router.register(r'estados', views.EstadoViewSet, basename='estados')
router.register(r'estados-detallados', views.EstadoDetalladoViewSet, basename='estados-detallados')
router.register(r'lugares', views.LugarViewSet, basename='lugares')
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'ministerios', views.MinisterioViewSet, basename='ministerios')
router.register(r'municipios', views.MunicipioViewSet, basename='municipios')
router.register(r'organizaciones-financieras', views.OrganizacionFinancieraViewSet, basename='organizaciones-financieras')
router.register(r'provincias', views.ProvinciaViewSet, basename='provincias')
router.register(r'responsables-contraparte', views.ResponsableContraparteViewSet, basename='responsables-contraparte')
router.register(r'roles', views.GroupViewSet, basename='roles')
router.register(r'sectores', views.SectorViewSet, basename='sectors')
router.register(r'tipos-financiamiento', views.TipoFinanciamientoViewSet, basename='tipos-financiamiento')
router.register(r'tipos-proyecto', views.TipoProyectoViewSet, basename='tipos-proyecto')
router.register(r'ucep-responsables', views.UcepResponsableViewSet, basename='ucep-responsable')
router.register(r'viceministerios', views.ViceministerioViewSet, basename='viceministerios')
router.register(r'sector-clasificador', views.SectoresClasificadorViewSet, basename='sector-clasificador')
router.register(r'sub-sector-clasificador', views.SubSectoresClasificadorViewSet, basename='sub-sector-clasificador')
router.register(r'estructuras-organizativas', views.EstructuraOrganizativaViewSet, basename='estructuras-organizativas')

urlpatterns = [
    path('sector-detallado/<int:pk>/', views.SectorDetalleViewSet.as_view(), name='sector-detalle'),
    path('', include(router.urls))
]

urlpatterns += router.urls  
