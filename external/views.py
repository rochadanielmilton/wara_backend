from django.shortcuts import render
from rest_framework import viewsets,filters,generics
from programas.models import Programas, Proyectos
from programas.serializers import ProgramasSerializer
from proyectos.serializers import ProyectosSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class ProgramasViewSet(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication] 
    permission_classes = [TokenHasReadWriteScope]
    queryset = Programas.objects.all()
    serializer_class = ProgramasSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['programas_proyectos']
    ordering = ['programas_proyectos']
    @swagger_auto_schema(
        operation_description="Obtiene una lista de programas. Requiere Authorization Bearer token.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER,
                description="Bearer token", 
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProyectosViewSet(generics.ListAPIView):
    authentication_classes = [OAuth2Authentication] 
    permission_classes = [TokenHasReadWriteScope]
    queryset = Proyectos.objects.all()
    serializer_class = ProyectosSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nombre']
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.query_params.get('nombre', None)
        nombre_viceministerio = self.request.query_params.get('nombre_viceministerio', None)
        anio_inicio = self.request.query_params.get('anio_inicio', None)
        anio_fin = self.request.query_params.get('anio_fin', None)
        estado = self.request.query_params.get('estado', None)
        emblematico = self.request.query_params.get('estado_emblematico', None)

        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        if nombre_viceministerio is not None:
            queryset = queryset.filter(viceministerio_id__nombre__icontains=nombre_viceministerio)
        if anio_inicio is not None and anio_fin is not None:
            queryset = queryset.filter(gestion__gte=anio_inicio, gestion__lte=anio_fin)
        if estado is not None:
            queryset = queryset.filter(estado_id=estado)
        if emblematico is not None:
            queryset = queryset.filter(emblematico=emblematico)

        return queryset
    
    @swagger_auto_schema(
        operation_description="Obtiene una lista de proyectos. Requiere Authorization Bearer token.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER,
                description="Bearer token", 
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)