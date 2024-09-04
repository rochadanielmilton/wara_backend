from rest_framework import serializers
from programas.models import *
from proyectos.models import *
from proyectos_preinversion.models import*
from decimal import Decimal

class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = ['id','nombre']

class ProvinciasSerializer(serializers.ModelSerializer):
    departamento = DepartamentosSerializer()

    class Meta:
        model = Provincias
        fields = ['id','nombre', 'departamento']

class MunicipiosSerializer(serializers.ModelSerializer):
    provincia = ProvinciasSerializer()

    class Meta:
        model = Municipios
        fields = ['id','nombre', 'provincia']


class LugaresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugares
        fields = ['id','nombre']

class OrganizacionesFinancierasSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizacionesFinancieras
        fields = ['id','sigla']

class EjecutoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejecutores
        fields = ['id','nombre']

class TiposProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposProyecto
        fields = ['id','nombre']

class EstadosProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estados2
        fields = ['id','nombre']

class ProgramasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programas
        fields = ['id','sigla']

class EmpresasConstructorasSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresasConstructoras
        fields = ['id','nombre']

class UcepResponsablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UcepResponsables
        fields = ['id','nombre']

class ProyectosSerializer(serializers.ModelSerializer):
    imagen_proyecto = serializers.ImageField(use_url=True, required=False)
    lugar_name = serializers.CharField(source='lugar.nombre', read_only=True)
    sector_name = serializers.CharField(source='sector.nombre', read_only=True)
    organizacion_name = serializers.CharField(source='organizacion.sigla', read_only=True)
    ejecutor_name = serializers.CharField(source='ejecutor.nombre', read_only=True)
    tipo_name = serializers.CharField(source='tipo.nombre', read_only=True)
    estado_name = serializers.CharField(source='estado.nombre', read_only=True)
    estado_detallado_nuevo_name = serializers.CharField(source='estado_detallado_nuevo.nombre', read_only=True)
    empresa_constructora_name = serializers.CharField(source='empresa_constructora.nombre', read_only=True)
    ucep_responsable_name = serializers.CharField(source='ucep_responsable.nombre', read_only=True)
    viceministerio_name = serializers.CharField(source='viceministerio.nombre',read_only=True)
    programa_sigla = serializers.CharField(source='programa.sigla_prog_convenio',read_only=True)
    sector_clasificador_name = serializers.SerializerMethodField()
    sub_sector_clasificador_name = serializers.SerializerMethodField()
    preinversion_name = serializers.CharField(source='preinversion.codigo_convenio',read_only=True)


    class Meta:
        model = Proyectos
        fields = '__all__'

    def get_sector_clasificador_name(self, obj):
        return obj.sector_clasificador.nombre if obj.sector_clasificador else None
    def get_sub_sector_clasificador_name(self, obj):
        return obj.sub_sector_clasificador.nombre if obj.sub_sector_clasificador else None

        
    def update(self, instance, validated_data):
        imagen_proyecto = validated_data.pop('imagen_proyecto', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if imagen_proyecto is not None:
            instance.imagen_proyecto = imagen_proyecto

        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            realizacion = Realizaciones.objects.filter(proyecto=instance).first()
            response['realizacion_id'] = realizacion.id if realizacion else None
        except Realizaciones.DoesNotExist:
            response['realizacion_id'] = None
        return response

class AguaSaneamientoSerializer(ProyectosSerializer):
    class Meta(ProyectosSerializer.Meta):
        fields = ['id','codigo_sisin','lugar','lugar_name','sector','sector_name','nombre','organizacion','empresa_constructora',
                  'empresa_constructora_name','organizacion_name','ejecutor','ejecutor_name','tipo','tipo_name','detalle','objetivo',
                  'estado_detallado','tipo_proyecto_detallado','fecha_inicio','fecha_conclusion','programa','programa_sigla',
                  'numero_familias_beneficiadas','numero_familias_indirectas','empleos_directos','preinversion','preinversion_name',
                  'empleos_indirectos','proyecto_cuenta_con_ptar','gobierno','beneficiados_varones',
                  'beneficiados_mujeres','observaciones','programado_para_entrega_por_efemeride','viceministerio',
                  'viceministerio_name','estado','estado_name','estado_detallado_nuevo','estado_detallado_nuevo_name',
                  'latitud','longitud','is_deleted','documento_creacion','imagen_proyecto','sector_clasificador',
                  'sector_clasificador_name','sub_sector_clasificador','sub_sector_clasificador_name','tipo_conflicto','descripcion_conflicto']
        
class CuencasSerializer(ProyectosSerializer):
    class Meta(ProyectosSerializer.Meta):
        fields = ['id','codigo_sisin','lugar','lugar_name','sector','sector_name','nombre','organizacion','organizacion_name',
                  'ejecutor','ejecutor_name','tipo','tipo_name','detalle','estado_detallado','fecha_inicio','fecha_conclusion',
                  'objetivo','tipo_proyecto_detallado','programa','programa_sigla','numero_familias_beneficiadas','numero_familias_indirectas',
                  'poblacion_beneficiaria_cuencas','numero_plantines','forestacion_ha','reforestacion_ha','superficie_plantada',
                  'viveros','empleos_directos','empleos_indirectos','observaciones','gobierno','beneficiados_varones','preinversion','preinversion_name',
                  'beneficiados_mujeres','programado_para_entrega_por_efemeride','viceministerio','viceministerio_name',
                  'fecha_inicio_cif','fecha_fin_cif','estado','estado_name','latitud','longitud','is_deleted','documento_creacion',
                  'emblematico','imagen_proyecto','sector_clasificador','sector_clasificador_name','sub_sector_clasificador',
                  'sub_sector_clasificador_name','tipo_conflicto','descripcion_conflicto']
        
class ResiduosSerializer(ProyectosSerializer):
    class Meta(ProyectosSerializer.Meta):
        fields = ['id','codigo_sisin','lugar','lugar_name','sector','sector_name','nombre','organizacion','organizacion_name',
                  'ejecutor','ejecutor_name','tipo','tipo_name','detalle','estado_detallado','objetivo','tipo_proyecto_detallado','fecha_inicio','fecha_conclusion',
                  'programa','programa_sigla','numero_familias_beneficiadas','numero_familias_indirectas','numero_plantines','preinversion','preinversion_name',
                  'forestacion_ha','toneladas_residuos_dispuestos_anio','toneladas_residuos_aprovechamiento_anio','empleos_directos',
                  'empleos_indirectos','empresa_constructora','empresa_constructora_name','ucep_responsable','ucep_responsable_name',
                  'observaciones','gobierno','beneficiados_varones','beneficiados_mujeres','objetivo','programado_para_entrega_por_efemeride',
                  'viceministerio','viceministerio_name','emblematico','estado','estado_name','latitud','longitud','is_deleted',
                  'documento_creacion','imagen_proyecto','sector_clasificador','sector_clasificador_name','sub_sector_clasificador',
                  'sub_sector_clasificador_name','tipo_conflicto','descripcion_conflicto']
        
class RiegoSerializer(ProyectosSerializer):
    class Meta(ProyectosSerializer.Meta):
        fields = ['id','codigo_sisin','lugar','lugar_name','sector','sector_name','nombre','organizacion','organizacion_name',
                  'ejecutor','ejecutor_name','tipo','tipo_name','detalle','estado_detallado','objetivo','tipo_proyecto_detallado','fecha_inicio','fecha_conclusion',
                  'programa','programa_sigla','numero_familias_beneficiadas','numero_familias_indirectas','superficie_riego_ha',
                  'empleos_directos','empleos_indirectos','ucep_responsable','ucep_responsable_name','observaciones','gobierno',
                  'beneficiados_varones','beneficiados_mujeres','objetivo','programado_para_entrega_por_efemeride','preinversion','preinversion_name',
                  'viceministerio','viceministerio_name','emblematico','estado','estado_name','latitud','longitud','is_deleted',
                  'documento_creacion','imagen_proyecto','sector_clasificador','sector_clasificador_name','sub_sector_clasificador',
                  'sub_sector_clasificador_name','tipo_conflicto','descripcion_conflicto']

class RealizacionesSerializer(serializers.ModelSerializer):
    #proyecto_id = serializers.IntegerField(write_only=True)
    departamento_name = serializers.CharField(source='departamento.nombre', read_only=True)
    provincia_name = serializers.CharField(source='provincia.nombre', read_only=True)
    municipio_name = serializers.CharField(source='municipio.nombre', read_only=True)
    estado_name = serializers.CharField(source='estado.nombre', read_only=True)

    # Nuevos campos para incluir los IDs de las tablas intermedias
    departamentos_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    provincias_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    municipios_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    # Campos para mostrar los IDs y nombres en las respuestas GET
    departamentos = serializers.SerializerMethodField()
    provincias = serializers.SerializerMethodField()
    municipios = serializers.SerializerMethodField()

    class Meta:
        model = Realizaciones
        fields = '__all__'

    def get_departamentos(self, obj):
        return [{'id': rd.departamento_id, 'nombre': rd.departamento.nombre} for rd in obj.realizaciondepartamentos_set.all()]

    def get_provincias(self, obj):
        return [{'id': rp.provincia_id, 'nombre': rp.provincia.nombre} for rp in obj.realizacionprovincias_set.all()]

    def get_municipios(self, obj):
        return [{'id': rm.municipio_id, 'nombre': rm.municipio.nombre} for rm in obj.realizacionmunicipios_set.all()]

    def create(self, validated_data):
        departamentos_ids = validated_data.pop('departamentos_ids', [])
        provincias_ids = validated_data.pop('provincias_ids', [])
        municipios_ids = validated_data.pop('municipios_ids', [])

        total_inversion = validated_data.get('total_inversion')
        validated_data['saldo_presupuesto'] = total_inversion
        validated_data['total_inversion_mill'] = total_inversion/1000000

        realizacion_instance = super().create(validated_data)

        for departamento_id in departamentos_ids:
            RealizacionDepartamentos.objects.create(realizacion=realizacion_instance, departamento_id=departamento_id)
        
        for provincia_id in provincias_ids:
            RealizacionProvincias.objects.create(realizacion=realizacion_instance, provincia_id=provincia_id)

        for municipio_id in municipios_ids:
            RealizacionMunicipios.objects.create(realizacion=realizacion_instance, municipio_id=municipio_id)

        return realizacion_instance

    def update(self, instance, validated_data):
        departamentos_ids = validated_data.pop('departamentos_ids', None)
        provincias_ids = validated_data.pop('provincias_ids', None)
        municipios_ids = validated_data.pop('municipios_ids', None)

        instance = super().update(instance, validated_data)

        if departamentos_ids is not None:
            RealizacionDepartamentos.objects.filter(realizacion=instance).delete()
            for departamento_id in departamentos_ids:
                RealizacionDepartamentos.objects.create(realizacion=instance, departamento_id=departamento_id)

        if provincias_ids is not None:
            RealizacionProvincias.objects.filter(realizacion=instance).delete()
            for provincia_id in provincias_ids:
                RealizacionProvincias.objects.create(realizacion=instance, provincia_id=provincia_id)

        if municipios_ids is not None:
            RealizacionMunicipios.objects.filter(realizacion=instance).delete()
            for municipio_id in municipios_ids:
                RealizacionMunicipios.objects.create(realizacion=instance, municipio_id=municipio_id)

        return instance
class IndicadoresUpdateSerializer(serializers.ModelSerializer):
    #proyecto_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Proyectos
        fields = [            
            'numero_familias_beneficiadas',
            'numero_familias_indirectas',
            'empleos_directos',
            'empleos_indirectos',
            'beneficiados_varones',
            'beneficiados_mujeres'
        ]
class SeguimientoSerializer(serializers.ModelSerializer):
    realizacion = serializers.PrimaryKeyRelatedField(queryset=Realizaciones.objects.all(), write_only=True)
    proyecto_name = serializers.CharField(source='realizacion.proyecto.nombre', read_only=True)
    
    fotografia_1 = serializers.ImageField(use_url=True, required=False, allow_null=True)
    fotografia_2 = serializers.ImageField(use_url=True, required=False, allow_null=True)
    fotografia_3 = serializers.ImageField(use_url=True, required=False, allow_null=True)
    fotografia_4 = serializers.ImageField(use_url=True, required=False, allow_null=True)
    documento_respaldo_avance = serializers.FileField(use_url=True, required=False, allow_null=True)
    
    class Meta:
        model = Seguimiento
        fields = '__all__'

    def validate(self, data):
        avance_financiero_mes = data.get('avance_financiero_mes')
        porcentaje_avance_fisico_mes = data.get('porcentaje_avance_fisico_mes')
        realizacion = data.get('realizacion')

        # Verificar si la realización está proporcionada
        if realizacion is None:
            raise serializers.ValidationError({'realizacion': 'La realización debe ser proporcionada.'})

        # Verificar el estado del proyecto
        if realizacion.proyecto.estado_id != 3:
            raise serializers.ValidationError({'message': 'El proyecto no se encuentra EN EJECUCIÓN, por tanto, no puede registrar un avance.'})

        # Validación del avance financiero del mes
        if avance_financiero_mes is not None and avance_financiero_mes < 0:
            raise serializers.ValidationError({'avance_financiero_mes': 'El avance financiero del mes debe ser positivo.'})

        # Validación del porcentaje de avance físico del mes
        if porcentaje_avance_fisico_mes is not None:
            if porcentaje_avance_fisico_mes < 0:
                raise serializers.ValidationError({'porcentaje_avance_fisico_mes': 'El porcentaje de avance físico del mes debe ser positivo.'})
            
            if porcentaje_avance_fisico_mes > (100 - realizacion.avance_fisico):
                raise serializers.ValidationError({'porcentaje_avance_fisico_mes': f'Le queda únicamente {(100 - realizacion.avance_fisico)}% por ejecutar.'})

        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['realizacion_id'] = instance.realizacion_id
        response['sector']=instance.realizacion.proyecto.sector.nombre
        return response

class ConexionSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Conexion
        exclude = ('proyecto',)
        read_only_fields = ['id', 'created_at', 'updated_at','proyecto_id']

class PoblacionSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Poblacion
        exclude = ('proyecto',)
        read_only_fields = ['id', 'proyecto_id', 'created_at', 'updated_at']

class DrenajePluvialSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = DrenajePluvial
        exclude = ('proyecto',)
        read_only_fields = ['id', 'proyecto_id', 'created_at', 'updated_at']

class VariableImpactoSerializer(serializers.ModelSerializer):
    proyecto_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = VariableImpacto
        exclude = ('proyecto',)
        read_only_fields = ['id', 'proyecto_id', 'created_at', 'updated_at']

