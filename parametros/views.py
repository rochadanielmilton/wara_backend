from logs.models import UserAction
from programas.models import RealizacionDepartamentos, RealizacionMunicipios, RealizacionProvincias,SubSectoresClasificador,SectoresClasificador
from .models import *
from .serializers import *
from .serializers import GroupSerializer
from authentication.models import Menu
from authentication.serializers import MenuSerializer
from backend_mmaya.views import SoftDeleteModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group
from rest_framework import generics, permissions
from rest_framework import generics,viewsets,status
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.db.models import Count,Q ,Subquery

class EmpresaConstructoraViewSet(SoftDeleteModelViewSet):
    queryset = EmpresaConstructora.objects.all()
    serializer_class = EmpresaConstructoraSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class SectoresClasificadorViewSet(SoftDeleteModelViewSet):
    queryset = SectoresClasificador.objects.all()
    serializer_class = SectoresClasificadorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class SubSectoresClasificadorViewSet(SoftDeleteModelViewSet):
    queryset = SubSectoresClasificador.objects.filter(is_deleted=False)
    serializer_class = SubSectoresClasificadorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class SectorViewSet(SoftDeleteModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    def get_queryset(self):
        queryset = super().get_queryset()
        viceministerio_id = self.request.query_params.get('viceministerio_id', None)
        if viceministerio_id:
            viceministerio_ids = viceministerio_id.split(',') if ',' in viceministerio_id else [viceministerio_id]
            queryset = queryset.filter(viceministerio__id__in=viceministerio_ids)
        return queryset

class SectorDetalleViewSet(generics.RetrieveAPIView):
    queryset = Sector.objects.all().prefetch_related('lugares','programas','ejecutores')
    serializer_class = SectorDetalladoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class AgenciaFinanciadoraViewSet(SoftDeleteModelViewSet):
    queryset = AgenciaFinanciadora.objects.all()
    serializer_class = AgenciaFinanciadoraSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class UcepResponsableViewSet(SoftDeleteModelViewSet):
    queryset=UcepResponsable.objects.all()
    serializer_class=UcepResponsableSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class TipoProyectoViewSet(SoftDeleteModelViewSet):
    queryset=TipoProyecto.objects.all()
    serializer_class=TipoProyectoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class TipoFinanciamientoViewSet(SoftDeleteModelViewSet):
    queryset=TipoFinanciamiento.objects.all()
    serializer_class=TipoFinanciamientoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class DepartamentoList(generics.ListAPIView):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Departamento.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProvinciaList(generics.ListAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('departamento_id',)
    
    def get_queryset(self):
        return Provincia.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MunicipioList(generics.ListAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('provincia_id',)
    
    def get_queryset(self):
        return Municipio.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class EstadoProyectoView(generics.ListAPIView):
    queryset = EstadoProyecto.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nombre']
    ordering = ['nombre'] 

class MenuViewSet(SoftDeleteModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        is_deleted = self.request.query_params.get('is_deleted', 'false')
        nombre = self.request.query_params.get('nombre', '')
        if is_deleted.lower() == 'false':
            queryset = queryset.filter(is_deleted=False)
        if nombre != '':
            queryset = queryset.filter(ruta__icontains=nombre)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        UserAction.log_action(
            user=request.user,
            action_name="Eliminar",
            instance=instance
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            if tipo=="MINISTERIO":
                queryset = queryset.exclude(name__icontains="SECTOR")
            if tipo=="SECTOR":
                queryset = queryset.filter(name__icontains="SECTOR")
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        UserAction.log_action(
            user=request.user,
            action_name="Eliminar",
            instance=instance
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class DepartamentoViewSet(SoftDeleteModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
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
    serializer_class = ProvinciaSerializer
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
    serializer_class = MunicipioSerializer
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
    serializer_class = OrganizacionFinancieraSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class EjecutorViewSet(SoftDeleteModelViewSet):
    queryset = Ejecutor.objects.all()
    serializer_class = EjecutorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class MinisterioViewSet(SoftDeleteModelViewSet):
    queryset = Ministerio.objects.all()
    serializer_class = MinisterioSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class ViceministerioViewSet(SoftDeleteModelViewSet):
    queryset = Viceministerio.objects.all().select_related('ministerio').prefetch_related('descentralizadas')
    serializer_class = ViceministerioSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        ministerio_id = self.request.query_params.get('ministerio_id', None)
        if ministerio_id:
            queryset = queryset.filter(ministerio_id=ministerio_id)
        return queryset

class DescentralizadaViewSet(SoftDeleteModelViewSet):
    queryset = Descentralizada.objects.all()
    serializer_class = DescentralizadaSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class EstadoViewSet(SoftDeleteModelViewSet):
    queryset = Estado2.objects.filter(is_deleted=False)
    serializer_class = EstadoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['id']
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
    serializer_class = EstadoDetalladoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        estado_id = self.request.query_params.get('estado_id', None)
        if estado_id:
            queryset = queryset.filter(estado_proyecto=estado_id)
        return queryset
    
class CargoViewSet(SoftDeleteModelViewSet):
    queryset = Cargo.objects.filter(is_deleted=False)
    serializer_class = CargoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['nombre']
    def get_queryset(self):
        queryset = super().get_queryset()
        estructura_organizativa_id = self.request.query_params.get('estructura_organizativa_id', None)
        if estructura_organizativa_id:
            queryset = queryset.filter(estructura_organizativa__id=estructura_organizativa_id)
        sector = self.request.query_params.get('sector', None)
        if sector:
            queryset = queryset.filter(nombre__icontains=f"SECTOR {sector}")
        return queryset

class ResponsableContraparteViewSet(SoftDeleteModelViewSet):
    queryset = ResponsableContraparte.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResposableContraparteSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class CoEjecutorViewSet(SoftDeleteModelViewSet):
    queryset = CoEjecutor.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CoEjecutoresSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']

class LugarViewSet(SoftDeleteModelViewSet):
    queryset=Lugar.objects.all()
    serializer_class=LugarSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class EstructuraOrganizativaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstructuraOrganizativa.objects.all()
    serializer_class = EstructuraOrganizativaSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['nombre']
    def get_queryset(self):
        queryset = super().get_queryset()
        area_id = self.request.query_params.get('area_id', None)
        if area_id:
            queryset = queryset.filter(area__id=area_id)
        return queryset