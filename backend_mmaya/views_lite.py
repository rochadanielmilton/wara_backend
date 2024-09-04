from logs.models import UserAction
from programas.models import RealizacionDepartamentos, RealizacionMunicipios, RealizacionProvincias,Programas
from parametros.models import *
from .serializers_lite import *
from backend_mmaya.views import SoftDeleteModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework import generics
from rest_framework import  filters
from rest_framework.response import Response
from django.db.models import Count,Subquery

class EmpresaConstructoraViewSet(SoftDeleteModelViewSet):
    queryset = EmpresaConstructora.objects.all()
    serializer_class = EmpresaConstructoraSelectSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']
    search_fields = ['nombre']

class SectorViewSet(SoftDeleteModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class SectorDetalleViewSet(generics.RetrieveAPIView):
    queryset = Sector.objects.all().prefetch_related('lugares','programas','ejecutores')
    serializer_class = SectorDetalladoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class AgenciaFinanciadoraViewSet(SoftDeleteModelViewSet):
    queryset = AgenciaFinanciadora.objects.all()
    serializer_class = AgenciaFinanciadoraSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'sigla']
    ordering = ['sigla']

class UcepResponsableViewSet(SoftDeleteModelViewSet):
    queryset=UcepResponsable.objects.all()
    serializer_class=UcepResponsableSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class TipoProyectoViewSet(SoftDeleteModelViewSet):
    queryset=TipoProyecto.objects.all()
    serializer_class=TipoProyectoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class TipoFinanciamientoViewSet(SoftDeleteModelViewSet):
    queryset=TipoFinanciamiento.objects.all()
    serializer_class=TipoFinanciamientoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class DepartamentoList(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSelectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        return Departamento.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProvinciaList(generics.ListAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSelectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('departamento_id',)
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        return Provincia.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MunicipioList(generics.ListAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSelectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('provincia_id',)
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        return Municipio.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class DepartamentoViewSet(SoftDeleteModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nombre']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        resource = self.request.query_params.get('resource', None)
        if resource:
            subquery = RealizacionDepartamentos.objects.values('departamento_id').annotate(
                dept_count=Count('departamento_id')
            ).filter(dept_count__gt=0).values('departamento_id')
            queryset = queryset.filter(id__in=Subquery(subquery))
        return queryset

class ProvinciaViewSet(SoftDeleteModelViewSet):
    queryset = Provincia.objects.all().prefetch_related('departamento')
    serializer_class = ProvinciaSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nombre', 'departamento__nombre']
    ordering = ['departamento__nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        resource = self.request.query_params.get('resource', None)
        departamento_id = self.request.query_params.get('departamento_id', None)
        if resource:
            subquery = RealizacionProvincias.objects.values('provincia_id').annotate(
                prov_count=Count('provincia_id')
            ).filter(prov_count__gt=0).values('provincia_id')
            queryset = queryset.filter(id__in=Subquery(subquery))
        if departamento_id:
            queryset = queryset.filter(departamento_id__in=departamento_id.split(","))
        return queryset
    
class MunicipioViewSet(SoftDeleteModelViewSet):
    queryset = Municipio.objects.all().prefetch_related('provincia','provincia__departamento')
    serializer_class = MunicipioSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['provincia__departamento__nombre', 'provincia__nombre','nombre']
    ordering = ['provincia__departamento__nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        resource = self.request.query_params.get('resource', None)
        provincia_id = self.request.query_params.get('provincia_id', None)
        if resource:
            subquery = RealizacionMunicipios.objects.values('municipio_id').annotate(
                mun_count=Count('municipio_id')
            ).filter(mun_count__gt=0).values('municipio_id')
            queryset = queryset.filter(id__in=Subquery(subquery))
        
        if provincia_id:
            queryset = queryset.filter(provincia_id__in=provincia_id.split(","))
        return queryset
    
class OrganizacionFinancieraViewSet(SoftDeleteModelViewSet):
    queryset = OrganizacionFinanciera.objects.all()
    serializer_class = OrganizacionFinancieraSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'sigla']
    ordering = ['sigla']

class EjecutorViewSet(SoftDeleteModelViewSet):
    queryset = Ejecutor.objects.all()
    serializer_class = EjecutorSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class MinisterioViewSet(SoftDeleteModelViewSet):
    queryset = Ministerio.objects.all()
    serializer_class = MinisterioSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']
class ProgramasViewSet(SoftDeleteModelViewSet):
    queryset = Programas.objects.all()
    serializer_class = ProgramasSelectSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id','sigla_prog_convenio']
    ordering = ['sigla_prog_convenio']
    search_fields = ['sigla_prog_convenio']

class ViceministerioViewSet(SoftDeleteModelViewSet):
    queryset = Viceministerio.objects.all().select_related('ministerio').prefetch_related('descentralizadas')
    serializer_class = ViceministerioSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        ministerio_id = self.request.query_params.get('ministerio_id', None)
        if ministerio_id:
            queryset = queryset.filter(ministerio_id=ministerio_id)
        return queryset

class DescentralizadaViewSet(SoftDeleteModelViewSet):
    queryset = Descentralizada.objects.all()
    serializer_class = DescentralizadaSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class EstadoViewSet(SoftDeleteModelViewSet):
    queryset = Estado2.objects.filter(is_deleted=False)
    serializer_class = EstadoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['nombre']
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_migrado = self.request.query_params.get('tipo_migrado')
        if tipo_migrado:
            tipo_migrado = tipo_migrado.strip().lower()
            if tipo_migrado == 'nuevo':
                queryset = queryset.filter(tipo__in=['nuevo', 'nuevo,migrado'])
            elif tipo_migrado == 'migrado':
                queryset = queryset.filter(tipo__in=['migrado', 'nuevo,migrado'])
            elif tipo_migrado == 'nuevo,migrado':
                queryset = queryset.filter(tipo=tipo_migrado)
        return queryset


class EstadoDetalladoViewSet(SoftDeleteModelViewSet):
    queryset = EstadoDetallado2.objects.filter(is_deleted=False).select_related('estado_proyecto')
    serializer_class = EstadoDetalladoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        estado_id = self.request.query_params.get('estado_id', None)
        if estado_id:
            queryset = queryset.filter(estado_proyecto=estado_id)
        return queryset
    
class CargoViewSet(SoftDeleteModelViewSet):
    queryset = Cargo.objects.filter(is_deleted=False)
    serializer_class = CargoSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class ResponsableContraparteViewSet(SoftDeleteModelViewSet):
    queryset = ResponsableContraparte.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResposableContraparteSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class CoEjecutorViewSet(SoftDeleteModelViewSet):
    queryset = CoEjecutor.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoEjecutoresSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class LugarViewSet(SoftDeleteModelViewSet):
    queryset=Lugar.objects.all()
    serializer_class=LugarSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']

class ProyectosPreinversionViewSet(SoftDeleteModelViewSet):
    queryset=ProyectosPreinversion.objects.all()
    serializer_class=PreinversionSelectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'nombre']
    ordering = ['nombre']
