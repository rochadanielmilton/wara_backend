from rest_framework import serializers

from administracion.models import Departamento
from backend_mmaya.serializers_lite import ProgramasSelectSerializer
from parametros.models import Ejecutor, Municipio, Provincia, UcepResponsable, Viceministerio
from parametros.serializers import OrganizacionFinancieraSerializer
from programas.models import Programas, TiposProyecto,Programa
from .models import Meta, MetaPreinversion, TiposProyectoPreinversion, EstadosPreinversion, Comunidades, PreinversionComunidad, PreinversionOrganismoFinanciador, ProyectosPreinversion
from programas.views import OrganizacionesFinancieras

class TiposProyectoPreinversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiposProyectoPreinversion
        fields = '__all__'

class EstadosPreinversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadosPreinversion
        fields = '__all__'

class ComunidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunidades
        fields = '__all__'

class PreinversionComunidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreinversionComunidad
        fields = '__all__'

class PreinversionOrganismoFinanciadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreinversionOrganismoFinanciador
        fields = '__all__'

class ProyectosPreinversionS1Serializer(serializers.Serializer):
    organismos_financiadores_ids = serializers.PrimaryKeyRelatedField(
        queryset=OrganizacionesFinancieras.objects.filter(is_deleted=False), 
        many=True, 
        source='organismos_financiadores'
    )
    codigo_convenio = serializers.CharField(max_length=20, allow_null=True)
    
    programa_id = serializers.PrimaryKeyRelatedField(queryset=Programa.objects.all(), required=False, allow_null=True)
    
    
    nombre =  serializers.CharField(max_length=200)

    estado_id = serializers.PrimaryKeyRelatedField(queryset=EstadosPreinversion.objects.filter(is_deleted=False))

    fecha_inicio = serializers.DateField(required=False, allow_null=True)
    fecha_conclusion = serializers.DateField(required=False, allow_null=True)

    codigo_sisin = serializers.CharField(max_length=16, allow_blank=True, allow_null=True, required=False)

    class Meta:
        fields = '__all__'

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_conclusion = data.get('fecha_conclusion')
        
        if fecha_conclusion and fecha_conclusion < fecha_inicio:
            raise serializers.ValidationError({
                'fecha_conclusion': 'La fecha de conclusión debe ser mayor o igual a la fecha de inicio.'
            })

        return data

    def validate_organismos_financiadores_ids(self, value):
        if not value:
            raise serializers.ValidationError("Seleccione al menos un organismo financiador.")
        return value

    
class ProyectosPreinversionS2Serializer(ProyectosPreinversionS1Serializer):
    viceministerio = serializers.PrimaryKeyRelatedField(queryset=Viceministerio.objects.filter(is_deleted=False), required=False, allow_null=True)
    sector = serializers.CharField(max_length=50)
    sub_sector = serializers.CharField(max_length=50)
    tipo_proyecto = serializers.PrimaryKeyRelatedField(queryset=TiposProyecto.objects.filter(is_deleted=False))
    departamento_id=serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.filter(is_deleted=False))
    provincia_id=serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.filter(is_deleted=False))
    municipio_id=serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.filter(is_deleted=False))
    comunidades_ids = serializers.PrimaryKeyRelatedField(      
                                        queryset=Comunidades.objects.filter(is_deleted=False), 
                                        required=False,
                                        allow_null=True,
                                        many=True, 
                                        source='comunidades'
                                   )
    
    def validate_comunidades_ids(self, value):
        if value is None:
            return []
        return value
    
class ProyectosPreinversionS3Serializer(ProyectosPreinversionS2Serializer):
    ucep_responsable_id = serializers.PrimaryKeyRelatedField(queryset=UcepResponsable.objects.filter(is_deleted=False),allow_null=True,required=False)
    ejecutor_id = serializers.PrimaryKeyRelatedField(queryset=Ejecutor.objects.filter(is_deleted=False))   
     
class ProyectosPreinversionSerializer(serializers.ModelSerializer):
    avance_financiero = serializers.FloatField(allow_null=True, required=False)
    comunidades_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    organismos_financiadores_ids = serializers.ListField(child=serializers.IntegerField(),write_only=True, required=False)
    departamento_id = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.filter(is_deleted=False))
    provincia_id = serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.filter(is_deleted=False))
    municipio_id = serializers.PrimaryKeyRelatedField(queryset=Municipio.objects.filter(is_deleted=False))
    ejecutor_id = serializers.PrimaryKeyRelatedField(queryset=Ejecutor.objects.filter(is_deleted=False))
    ejecutor_id = serializers.PrimaryKeyRelatedField(queryset=Ejecutor.objects.filter(is_deleted=False))
    programa_id = serializers.PrimaryKeyRelatedField(queryset=Programas.objects.filter(is_deleted=False), required=False, allow_null=True)
    avance_financiero = serializers.FloatField(allow_null=True, required=False)    

    def validate_avance_financiero(self, value):
        if value is not None and value > 100:
            raise serializers.ValidationError("El avance financiero no puede ser mayor a 100.")
        return value

    class Meta:
        model = ProyectosPreinversion
        exclude = ("departamento","provincia","municipio","ejecutor")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["comunidades"] = ComunidadesSerializer(instance.comunidades,many=True).data
        data["organismos_financiadores"] = OrganizacionFinancieraSerializer(instance.organismos_financiadores, many=True).data
        data["estado_texto"]=instance.estado
        data['estado'] = EstadosPreinversionSerializer(instance.estado_preinversion).data if instance.estado_preinversion else None
        data['programa'] =ProgramasSelectSerializer(instance.programa).data if instance.programa else None
        return data

    def create(self, validated_data):
        comunidades_ids = validated_data.pop('comunidades_ids', [])
        organismos_financiadores_ids = validated_data.pop('organismos_financiadores_ids', [])
        departamento = validated_data.pop("departamento_id")
        provincia = validated_data.pop("provincia_id")
        municipio = validated_data.pop("municipio_id")
        ejecutor = validated_data.pop("ejecutor_id")
        programa = validated_data.pop("programa_id",None)
        
        preinversion_instance = ProyectosPreinversion.objects.create(**validated_data,departamento=departamento,provincia=provincia,municipio=municipio,ejecutor=ejecutor,programa=programa)

        preinversion_comunidades = [
            PreinversionComunidad(comunidad_id=comunidad_id, preinversion_id=preinversion_instance.id)
            for comunidad_id in comunidades_ids
        ]
        PreinversionComunidad.objects.bulk_create(preinversion_comunidades)

        preinversion_organismos = [
            PreinversionOrganismoFinanciador(organismo_financiador_id=organismo_financiador_id, preinversion_id=preinversion_instance.id)
            for organismo_financiador_id in organismos_financiadores_ids
        ]
        PreinversionOrganismoFinanciador.objects.bulk_create(preinversion_organismos)

        return preinversion_instance
    
    def update(self, instance, validated_data):
        comunidades_ids = validated_data.pop('comunidades_ids',[])
        organismos_financiadores_ids = validated_data.pop('organismos_financiadores_ids',[])

        departamento = validated_data.pop("departamento_id")
        provincia = validated_data.pop("provincia_id")
        municipio = validated_data.pop("municipio_id")
        ejecutor = validated_data.pop("ejecutor_id")
        programa = validated_data.pop("programa_id",None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.departamento = departamento
        instance.provincia = provincia
        instance.municipio = municipio
        instance.ejecutor = ejecutor
        instance.programa = programa
        instance.save()
        # Actualizar los registros en SectorPrograma
        PreinversionComunidad.objects.filter(preinversion=instance).delete()
        PreinversionOrganismoFinanciador.objects.filter(preinversion=instance).delete()
        for comunidad_id in comunidades_ids:
            PreinversionComunidad.objects.create(comunidad_id=comunidad_id, preinversion_id=instance.id )

        for organismo_financiador_id in organismos_financiadores_ids:
            PreinversionOrganismoFinanciador.objects.create(organismo_financiador_id=organismo_financiador_id, preinversion_id=instance.id)

        return instance
    
class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = ('__all__')

class MetaPreinversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaPreinversion
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["meta_title"] = instance.meta.titulo
        return data