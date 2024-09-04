from rest_framework import viewsets, pagination,filters,status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from authentication.models import CustomUser
from logs.models import UserAction
from programas.models import Realizaciones,Seguimiento,Proyectos,RealizacionDepartamentos,RealizacionProvincias,RealizacionMunicipios
from proyectos.models import Conexion, DrenajePluvial, Poblacion, VariableImpacto
from .serializers import *
from decimal import Decimal
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.utils.timezone import now
from backend_mmaya.views import SoftDeleteModelViewSet, UpsertGetOneToOneViewSet
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, IntegerField, Q
class RealizacionesViewSet(SoftDeleteModelViewSet):
    queryset = Realizaciones.objects.all()
    serializer_class = RealizacionesSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'proyecto_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        sector_id = self.request.query_params.get('sector_id')
        proyecto_id = self.request.query_params.get('proyecto_id')

        if sector_id:
            queryset = queryset.filter(proyecto__sector_id=sector_id)
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)

        return queryset

    def create(self, request, *args, **kwargs):

        proyecto_id = request.data.get('proyecto')

        if not proyecto_id:
            return Response({"detail": "El campo 'proyecto' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            proyecto = Proyectos.objects.get(id=proyecto_id)
            estado_id = proyecto.estado_id

            request.data['estado'] = estado_id

        except Proyectos.DoesNotExist:
            return Response({"detail": "El proyecto especificado no existe."}, status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)



class ProyectosViewSet(SoftDeleteModelViewSet):
    queryset = Proyectos.objects.all().prefetch_related(
        'lugar', 'sector', 'organizacion', 'ejecutor', 'tipo', 'estado', 'empresa_constructora',
        'ucep_responsable', 'viceministerio', 'programa', 'sector_clasificador', 'sub_sector_clasificador'
    )
    serializer_class = ProyectosSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['id', 'created_at', 'updated_at', 'estado_id']
    search_fields = ['nombre', 'programa__programas_proyectos', 'programa__sigla_prog_convenio','codigo_sisin']

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.extra(
            select={'is_executing': 'estado_id = 3'}
        ).order_by('-is_executing', '-id')

        # Filtros adicionales
        nombre = self.request.query_params.get('nombre', None)
        viceministerio = self.request.query_params.get('viceministerio', None)
        gestion = self.request.query_params.get('gestion', None)
        estado = self.request.query_params.get('estado', None)
        emblematico = self.request.query_params.get('estado_emblematico', None)
        programa_id = self.request.query_params.get('programa_id', None)

        is_deleted = self.request.query_params.get('is_deleted', 'false')
        
        if is_deleted.lower() == 'false':
            queryset = queryset.filter(is_deleted=False)

        if self.request.user.is_viceministerio():
            queryset = queryset.filter(viceministerio=self.request.user.viceministerio)
        
        if self.request.user.is_descentralizada():
            queryset = queryset.filter(
                viceministerio_id=self.request.user.viceministerio.id, 
                ejecutor_id=self.request.user.descentralizada.id
            )

        if self.request.user.is_sector():
            queryset = queryset.filter(
                viceministerio_id=self.request.user.viceministerio.id, 
                sector_id=self.request.user.sector.id
            )
            
        if nombre is not None:
            queryset = queryset.filter(Q(nombre__icontains=nombre) | Q(codigo_sisin__icontains=nombre))
        if viceministerio is not None:
            queryset = queryset.filter(viceministerio_id__id=viceministerio)
        if gestion is not None and gestion is not None:
            queryset = queryset.filter(Q(fecha_inicio__year__icontains=gestion)|Q(fecha_conclusion__year__icontains=gestion))
        if estado is not None:
            queryset = queryset.filter(estado_id=estado)
        if emblematico is not None:
            queryset = queryset.filter(emblematico=emblematico)
        if programa_id is not None:
            queryset = queryset.filter(programa_id=programa_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Actualizar el estado de las realizaciones asociadas
        nuevo_estado_id = serializer.validated_data.get('estado')
        if nuevo_estado_id is not None:
            Realizaciones.objects.filter(proyecto=instance).update(estado_id=nuevo_estado_id)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


class RiegoProyectoViewSet(ProyectosViewSet):
    queryset = Proyectos.objects.filter(sector=1).prefetch_related('lugar','sector','organizacion','ejecutor','tipo','estado','empresa_constructora','ucep_responsable','viceministerio','programa','sector_clasificador','sub_sector_clasificador','preinversion')
    serializer_class = RiegoSerializer 
class AguaSaneamientoProyectoViewSet(ProyectosViewSet):
    queryset = Proyectos.objects.filter(sector=2).prefetch_related('lugar','sector','organizacion','ejecutor','tipo','estado','empresa_constructora','ucep_responsable','viceministerio','programa','sector_clasificador','sub_sector_clasificador','preinversion')
    serializer_class = AguaSaneamientoSerializer
class ResiduosProyectoViewSet(ProyectosViewSet):
    queryset = Proyectos.objects.filter(sector=3).prefetch_related('lugar','sector','organizacion','ejecutor','tipo','estado','empresa_constructora','ucep_responsable','viceministerio','programa','sector_clasificador','sub_sector_clasificador','preinversion')
    serializer_class = ResiduosSerializer
class CuencasProyectoViewSet(ProyectosViewSet):
    queryset = Proyectos.objects.filter(sector=4).prefetch_related('lugar','sector','organizacion','ejecutor','tipo','estado','empresa_constructora','ucep_responsable','viceministerio','programa','sector_clasificador','sub_sector_clasificador','preinversion')
    serializer_class = CuencasSerializer 
   

class UpdateIndicadoresAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        proyecto_id = request.query_params.get('proyecto_id')
        
        if proyecto_id:
            try:
                proyecto_instance = Proyectos.objects.get(id=proyecto_id)
                response_data = {
                    'numero_familias_beneficiadas': proyecto_instance.numero_familias_beneficiadas,
                    'numero_familias_indirectas': proyecto_instance.numero_familias_indirectas,
                    'empleos_directos': proyecto_instance.empleos_directos,
                    'empleos_indirectos': proyecto_instance.empleos_indirectos,
                    'beneficiados_varones': proyecto_instance.beneficiados_varones,
                    'beneficiados_mujeres': proyecto_instance.beneficiados_mujeres
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Proyectos.DoesNotExist:
                return Response({'message': 'No existe el proyecto seleccionado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'No se ingresó el id del proyecto'}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, *args, **kwargs):
        serializer = IndicadoresUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            proyecto_id = request.query_params.get('proyecto_id')
            
            try:
                proyecto_instance = Proyectos.objects.get(id=proyecto_id)
                
                for attr, value in serializer.validated_data.items():
                    if attr != 'proyecto_id':
                        setattr(proyecto_instance, attr, value)

                proyecto_instance.save()
                proyecto_serializer = ProyectosSerializer(proyecto_instance)
                return Response(proyecto_serializer.data, status=status.HTTP_200_OK)
            except Proyectos.DoesNotExist:
                return Response({'message': 'No se encontró el registro'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeguimientoViewSet(SoftDeleteModelViewSet):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['mes', 'anio']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_executing=Case(
                When(estado_seguimiento='pendiente', then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-is_executing', '-created_at')
        realizacion_id = self.request.query_params.get('realizacion_id', None)
        mes = self.request.query_params.get('mes', None)
        anio = self.request.query_params.get('anio', None)
        estado = self.request.query_params.get('estado_seguimiento',None)

        if hasattr(self.request.user, 'is_sector') and self.request.user.is_sector():
            sector_id = getattr(self.request.user, 'sector_id', None)
            if sector_id:
                queryset = queryset.filter(realizacion__proyecto__sector_id=sector_id)

        if realizacion_id is not None:
            queryset = queryset.filter(realizacion_id=realizacion_id)
        if mes is not None:
            queryset = queryset.filter(mes__icontains=mes)
        if anio is not None:
            queryset = queryset.filter(anio__icontains=anio)
        if estado is not None:
            queryset = queryset.filter(estado_seguimiento=estado)

        queryset = queryset.filter(is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        realizacion = validated_data.get('realizacion')

        try:
            realizacion_instance = Realizaciones.objects.get(id=realizacion.id)
        except Realizaciones.DoesNotExist:
            return Response({'message': 'Para el registro de seguimiento debe completar la información de Ejecuciones'}, status=status.HTTP_400_BAD_REQUEST)

        total_inversion = realizacion_instance.total_inversion
        total_ejecucion_acumulada = realizacion_instance.eje_acum
        avance_financiamiento = realizacion_instance.avance_financiamiento
        avance_fisico = realizacion_instance.avance_fisico
        saldo_presupuesto = realizacion_instance.saldo_presupuesto

        avance_financiero_mes = Decimal(validated_data.get('avance_financiero_mes', 0))
        porcentaje_avance_fisico_mes = Decimal(validated_data.get('porcentaje_avance_fisico_mes', 0))

        if saldo_presupuesto < avance_financiero_mes:
            return Response({'message': f'Le queda únicamente por ejecutar: {saldo_presupuesto}'}, status=status.HTTP_400_BAD_REQUEST)

        acumulado_financiero_mes = total_ejecucion_acumulada + avance_financiero_mes
        porcentaje_avance_financiero_mes = (avance_financiero_mes / total_inversion) * 100
        acumulado_porcentaje_financiero_mes = porcentaje_avance_financiero_mes + avance_financiamiento
        porcentaje_resto_financiero_mes = 100 - acumulado_porcentaje_financiero_mes
        acumulado_porcentaje_fisico_mes = porcentaje_avance_fisico_mes + avance_fisico
        porcentaje_resto_fisico_mes = 100 - acumulado_porcentaje_fisico_mes
        saldo_programado_proyecto = saldo_presupuesto - avance_financiero_mes

        validated_data.update({
            'total_programado_proyecto': total_inversion,
            'acumulado_financiero_mes': acumulado_financiero_mes,
            'porcentaje_avance_financiero_mes': porcentaje_avance_financiero_mes,
            'acumulado_porcentaje_financiero_mes': acumulado_porcentaje_financiero_mes,
            'porcentaje_resto_financiero_mes': porcentaje_resto_financiero_mes,
            'acumulado_porcentaje_fisico_mes': acumulado_porcentaje_fisico_mes,
            'porcentaje_resto_fisico_mes': porcentaje_resto_fisico_mes,
            'saldo_programado_proyecto': saldo_programado_proyecto,
        })

        if Seguimiento.objects.filter(realizacion=realizacion_instance, mes=validated_data.get('mes', 0), anio=validated_data.get('anio', 0), is_deleted=False):
            return Response({'message': 'El mes y año seleccionado ya registrado'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Seguimiento.objects.filter(realizacion=realizacion_instance, estado_seguimiento='pendiente', is_deleted=False):
                return Response({'message': 'Debe aprobar todos los seguimientos para registrar uno nuevo'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                try:
                    seguimiento_instance = Seguimiento.objects.create(**validated_data)

                    realizacion_instance.eje_acum = acumulado_financiero_mes
                    realizacion_instance.avance_fisico = acumulado_porcentaje_fisico_mes
                    realizacion_instance.avance_financiamiento = acumulado_porcentaje_financiero_mes
                    realizacion_instance.saldo_presupuesto = saldo_programado_proyecto
                    realizacion_instance.save()
                except Exception as e:
                    return Response({'message': 'Error al crear el seguimiento', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(SeguimientoSerializer(seguimiento_instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            seguimiento_instance = Seguimiento.objects.get(pk=pk)
            resetSeguimiento(pk)
            serializer = self.get_serializer(seguimiento_instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            # Recuperar instancia de realización relacionada
            realizacion_instance = seguimiento_instance.realizacion

            # Recalcular valores basados en los datos validados
            total_inversion = realizacion_instance.total_inversion
            total_ejecucion_acumulada = realizacion_instance.eje_acum
            avance_financiamiento = realizacion_instance.avance_financiamiento
            avance_fisico = realizacion_instance.avance_fisico
            saldo_presupuesto = realizacion_instance.saldo_presupuesto

            avance_financiero_mes = validated_data.get('avance_financiero_mes', seguimiento_instance.avance_financiero_mes)
            porcentaje_avance_fisico_mes = validated_data.get('porcentaje_avance_fisico_mes', seguimiento_instance.porcentaje_avance_fisico_mes)

            if saldo_presupuesto < avance_financiero_mes:
                return Response({'message': f'Le queda únicamente por ejecutar: {saldo_presupuesto}'}, status=status.HTTP_400_BAD_REQUEST)

            acumulado_financiero_mes = total_ejecucion_acumulada + avance_financiero_mes
            porcentaje_avance_financiero_mes = (avance_financiero_mes / total_inversion) * 100
            acumulado_porcentaje_financiero_mes = porcentaje_avance_financiero_mes + avance_financiamiento
            porcentaje_resto_financiero_mes = 100 - acumulado_porcentaje_financiero_mes
            acumulado_porcentaje_fisico_mes = porcentaje_avance_fisico_mes + avance_fisico
            porcentaje_resto_fisico_mes = 100 - acumulado_porcentaje_fisico_mes
            saldo_programado_proyecto = saldo_presupuesto - avance_financiero_mes

            # Actualizar valores recalculados en datos validados
            estado_seguimiento = seguimiento_instance.estado_seguimiento
            
            if estado_seguimiento == 'observado':
                estado_seguimiento ='subsanado'
            validated_data.update({
                'total_programado_proyecto': total_inversion,
                'acumulado_financiero_mes': acumulado_financiero_mes,
                'porcentaje_avance_financiero_mes': porcentaje_avance_financiero_mes,
                'acumulado_porcentaje_financiero_mes': acumulado_porcentaje_financiero_mes,
                'porcentaje_resto_financiero_mes': porcentaje_resto_financiero_mes,
                'acumulado_porcentaje_fisico_mes': acumulado_porcentaje_fisico_mes,
                'porcentaje_resto_fisico_mes': porcentaje_resto_fisico_mes,
                'saldo_programado_proyecto': saldo_programado_proyecto,
                'estado_seguimiento' : estado_seguimiento
            })

            # Actualizar instancia de seguimiento con datos validados
            for attr, value in validated_data.items():
                setattr(seguimiento_instance, attr, value)

            seguimiento_instance.save()

            # Actualizar instancia de realización relacionada
            realizacion_instance.eje_acum = acumulado_financiero_mes
            realizacion_instance.avance_fisico = acumulado_porcentaje_fisico_mes
            realizacion_instance.avance_financiamiento = acumulado_porcentaje_financiero_mes
            realizacion_instance.saldo_presupuesto = saldo_programado_proyecto
            realizacion_instance.save()

            return Response(SeguimientoSerializer(seguimiento_instance).data, status=status.HTTP_200_OK)
        except Seguimiento.DoesNotExist:
            return Response({'message': 'El seguimiento no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error al actualizar el seguimiento', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SeguimientoAdminViewSet(SoftDeleteModelViewSet):
    queryset = Seguimiento.objects.prefetch_related('realizacion','realizacion__proyecto','realizacion__proyecto__sector')
    serializer_class = SeguimientoSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['mes', 'anio']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_executing=Case(
                When(estado_seguimiento='pendiente', then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-is_executing', '-created_at')
        realizacion_id = self.request.query_params.get('realizacion_id', None)
        mes = self.request.query_params.get('mes', None)
        anio = self.request.query_params.get('anio', None)
        sector_id = self.request.query_params.get('sector_id', None)

        if sector_id is not None:
            queryset = queryset.filter(realizacion__proyecto__sector_id=sector_id)

        if realizacion_id is not None:
            queryset = queryset.filter(realizacion_id=realizacion_id)
        if mes is not None:
            queryset = queryset.filter(mes__icontains=mes)
        if anio is not None:
            queryset = queryset.filter(anio__icontains=anio)

        queryset = queryset.filter(is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        realizacion = validated_data.get('realizacion')

        try:
            realizacion_instance = Realizaciones.objects.get(id=realizacion.id)
        except Realizaciones.DoesNotExist:
            return Response({'message': 'Para el registro de seguimiento debe completar la información de Ejecuciones'}, status=status.HTTP_400_BAD_REQUEST)
        if realizacion_instance.proyecto.estado_id != 3:
            raise serializers.ValidationError({'message': 'El proyecto no se encuentra EN EJECUCIÓN, por tanto, no puede registrar un avance.'})
        total_inversion = realizacion_instance.total_inversion
        total_ejecucion_acumulada = realizacion_instance.eje_acum
        avance_financiamiento = realizacion_instance.avance_financiamiento
        avance_fisico = realizacion_instance.avance_fisico
        saldo_presupuesto = realizacion_instance.saldo_presupuesto

        avance_financiero_mes = Decimal(validated_data.get('avance_financiero_mes', 0))
        porcentaje_avance_fisico_mes = Decimal(validated_data.get('porcentaje_avance_fisico_mes', 0))

        if saldo_presupuesto < avance_financiero_mes:
            return Response({'message': f'Le queda únicamente por ejecutar: {saldo_presupuesto}'}, status=status.HTTP_400_BAD_REQUEST)

        acumulado_financiero_mes = total_ejecucion_acumulada + avance_financiero_mes
        porcentaje_avance_financiero_mes = (avance_financiero_mes / total_inversion) * 100
        acumulado_porcentaje_financiero_mes = porcentaje_avance_financiero_mes + avance_financiamiento
        porcentaje_resto_financiero_mes = 100 - acumulado_porcentaje_financiero_mes
        acumulado_porcentaje_fisico_mes = porcentaje_avance_fisico_mes + avance_fisico
        porcentaje_resto_fisico_mes = 100 - acumulado_porcentaje_fisico_mes
        saldo_programado_proyecto = saldo_presupuesto - avance_financiero_mes

        validated_data.update({
            'total_programado_proyecto': total_inversion,
            'acumulado_financiero_mes': acumulado_financiero_mes,
            'porcentaje_avance_financiero_mes': porcentaje_avance_financiero_mes,
            'acumulado_porcentaje_financiero_mes': acumulado_porcentaje_financiero_mes,
            'porcentaje_resto_financiero_mes': porcentaje_resto_financiero_mes,
            'acumulado_porcentaje_fisico_mes': acumulado_porcentaje_fisico_mes,
            'porcentaje_resto_fisico_mes': porcentaje_resto_fisico_mes,
            'saldo_programado_proyecto': saldo_programado_proyecto,
        })

        if Seguimiento.objects.filter(realizacion=realizacion_instance, mes=validated_data.get('mes', 0), anio=validated_data.get('anio', 0), is_deleted=False):
            return Response({'message': 'El mes y año seleccionado ya registrado'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if Seguimiento.objects.filter(realizacion=realizacion_instance, estado_seguimiento='pendiente', is_deleted=False):
                return Response({'message': 'Debe aprobar todos los seguimientos para registrar uno nuevo'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                try:
                    seguimiento_instance = Seguimiento.objects.create(**validated_data)

                    realizacion_instance.eje_acum = acumulado_financiero_mes
                    realizacion_instance.avance_fisico = acumulado_porcentaje_fisico_mes
                    realizacion_instance.avance_financiamiento = acumulado_porcentaje_financiero_mes
                    realizacion_instance.saldo_presupuesto = saldo_programado_proyecto
                    realizacion_instance.save()
                except Exception as e:
                    return Response({'message': 'Error al crear el seguimiento', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(SeguimientoSerializer(seguimiento_instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            seguimiento_instance = Seguimiento.objects.get(pk=pk)
            resetSeguimiento(pk)
            serializer = self.get_serializer(seguimiento_instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            # Recuperar instancia de realización relacionada
            realizacion_instance = seguimiento_instance.realizacion

            # Recalcular valores basados en los datos validados
            total_inversion = realizacion_instance.total_inversion
            total_ejecucion_acumulada = realizacion_instance.eje_acum
            avance_financiamiento = realizacion_instance.avance_financiamiento
            avance_fisico = realizacion_instance.avance_fisico
            saldo_presupuesto = realizacion_instance.saldo_presupuesto

            avance_financiero_mes = validated_data.get('avance_financiero_mes', seguimiento_instance.avance_financiero_mes)
            porcentaje_avance_fisico_mes = validated_data.get('porcentaje_avance_fisico_mes', seguimiento_instance.porcentaje_avance_fisico_mes)

            if saldo_presupuesto < avance_financiero_mes:
                return Response({'message': f'Le queda únicamente por ejecutar: {saldo_presupuesto}'}, status=status.HTTP_400_BAD_REQUEST)

            acumulado_financiero_mes = total_ejecucion_acumulada + avance_financiero_mes
            porcentaje_avance_financiero_mes = (avance_financiero_mes / total_inversion) * 100
            acumulado_porcentaje_financiero_mes = porcentaje_avance_financiero_mes + avance_financiamiento
            porcentaje_resto_financiero_mes = 100 - acumulado_porcentaje_financiero_mes
            acumulado_porcentaje_fisico_mes = porcentaje_avance_fisico_mes + avance_fisico
            porcentaje_resto_fisico_mes = 100 - acumulado_porcentaje_fisico_mes
            saldo_programado_proyecto = saldo_presupuesto - avance_financiero_mes

            # Actualizar valores recalculados en datos validados
            validated_data.update({
                'total_programado_proyecto': total_inversion,
                'acumulado_financiero_mes': acumulado_financiero_mes,
                'porcentaje_avance_financiero_mes': porcentaje_avance_financiero_mes,
                'acumulado_porcentaje_financiero_mes': acumulado_porcentaje_financiero_mes,
                'porcentaje_resto_financiero_mes': porcentaje_resto_financiero_mes,
                'acumulado_porcentaje_fisico_mes': acumulado_porcentaje_fisico_mes,
                'porcentaje_resto_fisico_mes': porcentaje_resto_fisico_mes,
                'saldo_programado_proyecto': saldo_programado_proyecto,
                'estado_seguimiento':'pendiente'
            })

            # Actualizar instancia de seguimiento con datos validados
            for attr, value in validated_data.items():
                setattr(seguimiento_instance, attr, value)

            seguimiento_instance.save()

            # Actualizar instancia de realización relacionada
            realizacion_instance.eje_acum = acumulado_financiero_mes
            realizacion_instance.avance_fisico = acumulado_porcentaje_fisico_mes
            realizacion_instance.avance_financiamiento = acumulado_porcentaje_financiero_mes
            realizacion_instance.saldo_presupuesto = saldo_programado_proyecto
            realizacion_instance.save()

            return Response(SeguimientoSerializer(seguimiento_instance).data, status=status.HTTP_200_OK)
        except Seguimiento.DoesNotExist:
            return Response({'message': 'El seguimiento no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error al actualizar el seguimiento', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class bajaSeguimientoEspecificoAPIView(APIView):
    def put(self, request, *args,**kwargs):
        seguimiento_id = request.query_params.get('seguimiento_id')
        if seguimiento_id:
            try:
                seguimiento_instance=Seguimiento.objects.get(id=seguimiento_id)
                if seguimiento_instance and seguimiento_instance.is_deleted==True:
                        return Response({'message':'El registro ya se dio baja anteriormente'})
                ejecutado_financiero_mes=seguimiento_instance.avance_financiero_mes
                porcentaje_financiero_mes=seguimiento_instance.porcentaje_avance_financiero_mes
                porcentaje_fisico_mes=seguimiento_instance.porcentaje_avance_fisico_mes

                realizacion_instance = Realizaciones.objects.get(id=seguimiento_instance.realizacion_id)
            except:
                return Response({'message':'hubo un error al dar baja un seguimiento'},status=status.HTTP_400_BAD_REQUEST)

        realizacion_instance.avance_fisico = Decimal(realizacion_instance.avance_fisico)-porcentaje_fisico_mes
        realizacion_instance.avance_financiamiento = Decimal(realizacion_instance.avance_financiamiento)-porcentaje_financiero_mes
        realizacion_instance.saldo_presupuesto += ejecutado_financiero_mes
        realizacion_instance.eje_acum = Decimal(realizacion_instance.eje_acum)-ejecutado_financiero_mes
        realizacion_instance.save()
                
        # seguimiento_instance.is_deleted=True
        seguimiento_instance.save()

        return Response({'message':'Se dio baja correctamente al registro del seguimiento'},status=status.HTTP_200_OK)
def resetSeguimiento(seguimiento_id):
    if seguimiento_id:
            try:
                seguimiento_instance=Seguimiento.objects.get(id=seguimiento_id)
                if seguimiento_instance and seguimiento_instance.is_deleted==True:
                        return Response({'message':'El registro ya se dio baja anteriormente'})
                ejecutado_financiero_mes=seguimiento_instance.avance_financiero_mes
                porcentaje_financiero_mes=seguimiento_instance.porcentaje_avance_financiero_mes
                porcentaje_fisico_mes=seguimiento_instance.porcentaje_avance_fisico_mes

                realizacion_instance = Realizaciones.objects.get(id=seguimiento_instance.realizacion_id)
            except:
                return Response({'message':'hubo un error al dar baja un seguimiento'},status=status.HTTP_400_BAD_REQUEST)

            realizacion_instance.avance_fisico -= porcentaje_fisico_mes
            realizacion_instance.avance_financiamiento -= porcentaje_financiero_mes
            realizacion_instance.saldo_presupuesto += ejecutado_financiero_mes
            realizacion_instance.eje_acum -= ejecutado_financiero_mes
            realizacion_instance.save()
                
            # seguimiento_instance.is_deleted=True
            # seguimiento_instance.save()
            return True
    else:
        return False
class SeguimientoParaValidacionView(APIView):
    def get(self, request, pk=None):
        seguimiento_actual = get_object_or_404(Seguimiento, pk=pk, is_deleted=False)
        seguimiento_anterior = Seguimiento.objects.filter(
            realizacion=seguimiento_actual.realizacion,
            created_at__lt=seguimiento_actual.created_at,
            is_deleted=False
        ).order_by('-created_at').first()
        
        # Pasar el contexto de la solicitud al serializador
        serializer_actual = SeguimientoSerializer(seguimiento_actual, context={'request': request})
        serializer_anterior = SeguimientoSerializer(seguimiento_anterior, context={'request': request}) if seguimiento_anterior else None
        
        data = {
            'actual': serializer_actual.data,
            'anterior': serializer_anterior.data if serializer_anterior else None
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reporte_ficha_tecnica_pdf(request):
    realizacion_id = request.GET.get('realizacion_id')

    if not realizacion_id:
        return JsonResponse({'message': 'No se proporcionó el ID de la realización'}, status=400)

    try:
        realizacion_instance = Realizaciones.objects.get(id=realizacion_id)
    except Realizaciones.DoesNotExist:
        return JsonResponse({'message': 'El registro no se encuentra'}, status=404)

    # Obtener los nombres de los departamentos, provincias y municipios
    departamentos = [{'nombre': rd.departamento.nombre} for rd in realizacion_instance.realizaciondepartamentos_set.all()]
    provincias = [{'nombre': rp.provincia.nombre} for rp in realizacion_instance.realizacionprovincias_set.all()]
    municipios = [{'nombre': rm.municipio.nombre} for rm in realizacion_instance.realizacionmunicipios_set.all()]

    # Obtener los seguimientos asociados
    seguimiento = Seguimiento.objects.filter(realizacion_id=realizacion_instance)

    template_path = 'reporte-ficha-tecnica.html'
    base_url = f"{request.scheme}://{request.get_host()}"
    context = {
        'usuario':request.user,
        'base_url': base_url,
        'current_datetime': now(),
        'realizacion_instance': realizacion_instance,
        'departamentos': departamentos,
        'provincias': provincias,
        'municipios': municipios,
        'seguimientos': seguimiento
    }
    
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF: {}'.format(pisa_status.err))

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reporte_avance_proyecto_pdf(request):
    realizacion_id = request.GET.get('realizacion_id')

    if not realizacion_id:
        return JsonResponse({'message': 'No se proporcionó el ID de la realización'}, status=400)

    try:
        realizacion_instance = Realizaciones.objects.get(id=realizacion_id)
    except Realizaciones.DoesNotExist:
        return JsonResponse({'message':'El registro no se encuentra'},status=404)
    departamentos = [{'nombre': rd.departamento.nombre} for rd in realizacion_instance.realizaciondepartamentos_set.all()]
    provincias = [{'nombre': rp.provincia.nombre} for rp in realizacion_instance.realizacionprovincias_set.all()]
    municipios = [{'nombre': rm.municipio.nombre} for rm in realizacion_instance.realizacionmunicipios_set.all()]
    if realizacion_instance:
        seguimiento = Seguimiento.objects.filter(realizacion_id=realizacion_instance).filter(is_deleted=False)
    else:
        seguimiento={}
    
    template_path = 'reporte-seguimiento-proyecto.html'
    base_url = f"{request.scheme}://{request.get_host()}"
    context = {
        'usuario':request.user,
        'base_url': base_url,
        'current_datetime':now(),
        'realizacion_instance':realizacion_instance,
        'departamentos': departamentos,
        'provincias': provincias,
        'municipios': municipios,
        'seguimientos':seguimiento

    }
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF: {}'.format(pisa_status.err))

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reporte_seguimiento_mensual_pdf(request):
    seguimiento_id = request.GET.get('seguimiento_id')

    if not seguimiento_id:
        return JsonResponse({'message': 'No se proporcionó el ID de la realización'}, status=400)

    try:
        seguimiento_instance = Seguimiento.objects.get(id=seguimiento_id)
    except Seguimiento.DoesNotExist:
        return JsonResponse({'message':'El registro no se encuentra'},status=404)
    
    if seguimiento_instance:
        realizacion_instance = Realizaciones.objects.filter(id=seguimiento_instance.realizacion_id).first()
    else:
        realizacion_instance={}
    departamentos = [{'nombre': rd.departamento.nombre} for rd in realizacion_instance.realizaciondepartamentos_set.all()]
    provincias = [{'nombre': rp.provincia.nombre} for rp in realizacion_instance.realizacionprovincias_set.all()]
    municipios = [{'nombre': rm.municipio.nombre} for rm in realizacion_instance.realizacionmunicipios_set.all()]
    template_path = 'reporte-seguimiento-proyecto-mensual.html'
    base_url = f"{request.scheme}://{request.get_host()}"
    context = {
        'usuario':request.user,
        'base_url': base_url,
        'current_datetime':now(),
        'seguimiento_instance':seguimiento_instance,
        'realizacion_instance':realizacion_instance,
        'departamentos':departamentos,
        'provincias':provincias,
        'municipios':municipios

    }
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF: {}'.format(pisa_status.err))

    return response

class ConexionesViewSet(UpsertGetOneToOneViewSet):
    queryset = Conexion.objects.all()
    serializer_class = ConexionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'proyecto_id'

class PoblacionesViewSet(UpsertGetOneToOneViewSet):
    queryset = Poblacion.objects.all()
    serializer_class = PoblacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'proyecto_id'
    
class DrenajesPluvialesViewSet(UpsertGetOneToOneViewSet):
    queryset = DrenajePluvial.objects.all()
    serializer_class = DrenajePluvialSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'proyecto_id'
    
class VariablesImpactoViewSet(UpsertGetOneToOneViewSet):
    queryset = VariableImpacto.objects.all()
    serializer_class = VariableImpactoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'proyecto_id'
    
class obtenerFichaTecnicaView(APIView):
    def get(self, request, *args, **kwargs):
        realizacion_id = request.query_params.get('realizacion_id')
        if realizacion_id:
            try:
                realizacion_instance = Realizaciones.objects.get(id=realizacion_id)
            except Realizaciones.DoesNotExist:
                return Response({'message':'no se econtro un proyecto especifico con ese id'}, status=status.HTTP_404_NOT_FOUND)
        
        realizacion_serializer = RealizacionesSerializer(realizacion_instance, context={'request': request})
        try:
            proyecto_instance = Proyectos.objects.get(id=realizacion_instance.proyecto_id)
        except Proyectos.DoesNotExist:
            return Response({'message':'no se encontro datos de proyecto general'}, status=status.HTTP_404_NOT_FOUND)
        
        proyecto_serializer = ProyectosSerializer(proyecto_instance, context={'request': request})

        response_data = {
            'proyecto_general': proyecto_serializer.data,
            'proyecto_especifico': realizacion_serializer.data
        }

        return Response(response_data)
    
class actualizarGeorreferenciacionAPIView(APIView):
    def put(self,request,*args,**kwargs):
        proyecto_id = request.query_params.get('proyecto_id')
        latitud =request.query_params.get('latitud')
        longitud = request.query_params.get('longitud')
        if proyecto_id:
            try:
                proyecto_instance = Proyectos.objects.get(id=proyecto_id)
            except Proyectos.DoesNotExist:
                return Response({'message':'No se Encontro un proyecto con el id proporcionado'},status=status.HTTP_404_NOT_FOUND)
        proyecto_instance.latitud = latitud
        proyecto_instance.longitud = longitud
        proyecto_instance.save()
        
        proyecto_serializer=ProyectosSerializer(proyecto_instance).data
        return Response(proyecto_serializer,status=status.HTTP_200_OK)
    
        
    

class aprobacionSeguimientoAPIView(APIView):
    def put(self,request, *args, **kwargs):
        seguimiento_id = request.query_params.get('seguimiento_id')
        if seguimiento_id:
            try:
                seguimiento_instance = Seguimiento.objects.get(id=seguimiento_id)
                if seguimiento_instance.estado_seguimiento == 'aprobado':
                    return Response({'message':'No puede aprobar mas de una ves un seguimiento'},status=status.HTTP_400_BAD_REQUEST)
                seguimiento_instance.estado_seguimiento = 'aprobado'
                seguimiento_instance.save()
            except Seguimiento.DoesNotExist:
                return Response({'message':'No se encontro el registro'},status=status.HTTP_404_NOT_FOUND)
        seguimiento_serializer = SeguimientoSerializer(seguimiento_instance).data  
        return Response(seguimiento_serializer,status=200)
    

class rechazarSeguimientoAPIView(APIView):
    def put(self,request,*args,**kwargs):
        seguimiento_id = request.query_params.get('seguimiento_id')
        observacion = request.query_params.get('observacion')
        if seguimiento_id and observacion:
            try:
                seguimiento_instance = Seguimiento.objects.get(id=seguimiento_id)
                if seguimiento_instance.estado_seguimiento == 'observado':
                    return Response({'message':'El proyecto ya se encuentra observado'},status=status.HTTP_400_BAD_REQUEST)
                seguimiento_instance.estado_seguimiento = 'observado'
                seguimiento_instance.observacion_estado = observacion
                seguimiento_instance.save()
                return Response({'message':'Seguimiento observado...'})
            except Seguimiento.DoesNotExist:
                return Response({'message':'No se encontro el registro'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message':'Debe ingresar el seguimiento y observación'},status=status.HTTP_400_BAD_REQUEST)
            
