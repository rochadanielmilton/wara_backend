from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from logs.models import UserAction
from programas.mixin import MultipleFieldLookupMixin
from programas.models import OrganizacionesFinancieras
from .models import Meta, MetaPreinversion, TiposProyectoPreinversion, EstadosPreinversion, Comunidades, PreinversionComunidad, PreinversionOrganismoFinanciador, ProyectosPreinversion
from .serializers import MetaPreinversionSerializer, MetaSerializer, ProyectosPreinversionS1Serializer, ProyectosPreinversionS2Serializer, ProyectosPreinversionS3Serializer, TiposProyectoPreinversionSerializer, EstadosPreinversionSerializer, ComunidadesSerializer, PreinversionComunidadSerializer, PreinversionOrganismoFinanciadorSerializer, ProyectosPreinversionSerializer
from backend_mmaya.views import SoftDeleteModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework import status, filters, permissions, generics
from django.db.models import Q

class TiposProyectoPreinversionViewSet(SoftDeleteModelViewSet):
    queryset = TiposProyectoPreinversion.objects.all()
    serializer_class = TiposProyectoPreinversionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['nombre']

class EstadosPreinversionViewSet(SoftDeleteModelViewSet):
    queryset = EstadosPreinversion.objects.all()
    serializer_class = EstadosPreinversionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

class ComunidadesViewSet(SoftDeleteModelViewSet):
    queryset = Comunidades.objects.all()
    serializer_class = ComunidadesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at','nombre']
    ordering = ['nombre']
    def get_queryset(self):
        queryset = super().get_queryset()
        municipio_id = self.request.query_params.get('municipio_id',None)
        if municipio_id:
            queryset = queryset.filter(municipio__id=municipio_id)
        return queryset


class PreinversionComunidadViewSet(SoftDeleteModelViewSet):
    queryset = PreinversionComunidad.objects.all()
    serializer_class = PreinversionComunidadSerializer
    filter_backends = [filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['nombre','sector','sub_sector']
    ordering = ['-created_at']


class PreinversionOrganismoFinanciadorViewSet(SoftDeleteModelViewSet):
    queryset = PreinversionOrganismoFinanciador.objects.all()
    serializer_class = PreinversionOrganismoFinanciadorSerializer

class ProyectosPreinversionViewSet(SoftDeleteModelViewSet):
    queryset = ProyectosPreinversion.objects.all() \
        .prefetch_related(
            'comunidades',
            'organismos_financiadores',
            'estado_preinversion',
            'programa'
        )
    serializer_class = ProyectosPreinversionSerializer
    filter_backends = [filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    ordering = ['-id']

    def get_serializer_class(self):
        paso = self.request.query_params.get("paso",None)
        if not paso:
            return ProyectosPreinversionSerializer
        if paso not in ["1","2","3","4","5"]:
            raise ValidationError("Paso debe estar entre 1 y 5")
        if paso == "1":
            return ProyectosPreinversionS1Serializer
        if paso == "2":
            return ProyectosPreinversionS2Serializer
        if paso == "3":
            return ProyectosPreinversionS3Serializer
        # if paso == "4":
        #     return ProyectosPreinversionS4Serializer
        if paso == "4":
            return ProyectosPreinversionSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        programa = self.request.query_params.get('programa_id', None)
        if programa:
            queryset = queryset.filter(programa__id=programa)
        if search:    
            queryset = queryset.filter(
                Q(nombre__icontains=search) | 
                Q(programa__sigla_prog_convenio__icontains=search) |
                Q(codigo_convenio__icontains=search)
            )       
        return queryset
    def create(self, request, *args, **kwargs):
        paso = request.query_params.get("paso", "1")
        data=request.data.copy()
        data["estado_preinversion"] = request.data.get("estado_id")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        if paso in ["1","2","3"]:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        if paso == "4":
            serializer.save()
            UserAction.log_action(
                user=request.user,
                action_name="Crear",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        paso = request.query_params.get("paso", "1")
        instance = self.get_object()
        data = request.data.copy()
        if "programa" in data:
            del data["programa"]

        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)

        if paso in ["1","2","3"]:
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        if paso == "4":
            serializer.save()
            UserAction.log_action(
                user=request.user,
                action_name="Actualizar",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class MetaViewSet(viewsets.ModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['titulo']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['titulo']

class MetaPreinversionListView(generics.ListAPIView):
    serializer_class = MetaPreinversionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        preinversion_id = self.kwargs['preinversion_id']
        return MetaPreinversion.objects.filter(preinversion_id=preinversion_id).prefetch_related('meta')

class MetaPreinversionDetailView(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = MetaPreinversion.objects.all()
    serializer_class = MetaPreinversionSerializer
    multiple_lookup_fields = ['preinversion_id', 'meta_id']
    permission_classes = [permissions.IsAuthenticated]
    
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
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            instance = None

        preinversion_id = kwargs.get('preinversion_id')
        meta_id = kwargs.get('meta_id')
        preinversion = get_object_or_404(ProyectosPreinversion, id=preinversion_id)
        meta = get_object_or_404(Meta, id=meta_id)
        data = request.data.copy()
        data['preinversion'] = preinversion.id
        data['meta'] = meta.id

        if instance:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            UserAction.log_action(
                user=request.user,
                action_name="Actualizar",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            UserAction.log_action(
                user=request.user,
                action_name="Crear",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)