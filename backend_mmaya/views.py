from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from logs.models import Action, UserAction
from django.core.serializers import serialize
from drf_yasg import openapi

class SoftDeleteModelViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_description="Obtiene una lista del recurso.",
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Qué campo utilizar al ordenar.",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Un número de página dentro del conjunto de resultados paginados.",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Número de resultados a devolver por página.",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        UserAction.log_action(
            user=request.user,
            action_name="Crear",
            instance=self.queryset.get(pk=serializer.data['id'])
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        UserAction.log_action(
            user=request.user,
            action_name="Actualizar",
            instance=instance
        )

        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        is_deleted = self.request.query_params.get('is_deleted', 'false')
        estado = self.request.query_params.get('estado', None)
        nombre = self.request.query_params.get('nombre', None)
        
        if is_deleted.lower() == 'false':
            queryset = queryset.filter(is_deleted=False)
        if estado is not None:
            queryset = queryset.filter(estado=estado)
        if nombre is not None:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset

        
    
class UpsertGetOneToOneViewSet(generics.RetrieveUpdateAPIView):
    def get_object(self):
        try:
            return self.queryset.get(**{
                self.lookup_url_kwarg:self.kwargs.get(self.lookup_url_kwarg) 
            })
        except ObjectDoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            data = request.data.copy()
            data[self.lookup_url_kwarg] = self.kwargs.get(self.lookup_url_kwarg)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            UserAction.log_action(
                user=request.user,
                action_name="Crear",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = request.data.copy()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            UserAction.log_action(
                user=request.user,
                action_name="Actualizar",
                instance=instance
            )
            return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()