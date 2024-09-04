from rest_framework import serializers
from proyectos_preinversion.models import ProyectosPreinversion
from parametros.models import SectorPrograma,Sector
from proyectos_preinversion.models import ProyectosPreinversion
# from parametros.serializers import SectorSerializer
# from proyectos_preinversion.models import ProyectosPreinversion
from .models import Objetivo, ObjetivoPrograma, Programas, TipoPrograma,Proyectos

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ('id', 'nombre', 'estado', 'created_at', 'updated_at', 'is_deleted')
class ProgramasSerializer(serializers.ModelSerializer):
    sector_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    sectores = serializers.SerializerMethodField()  # Campo adicional para los sectores
    numero_proyectos = serializers.IntegerField(
        source='proyectos_set.count', 
        read_only=True
    )

    class Meta:
        model = Programas
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["numero_preinversiones"] = ProyectosPreinversion.objects.filter(programa__id=instance.id).count()
        return data

    def get_sectores(self, obj):
        sectores = obj.sectorprograma_set.all()
        return [{'id': sp.sector.id, 'nombre': sp.sector.nombre} for sp in sectores]

    def create(self, validated_data):
        sector_ids = validated_data.pop('sector_ids', [])
        programa_instance = Programas.objects.create(**validated_data)

        # Crear registros en SectorPrograma para cada sector relacionado
        for sector_id in sector_ids:
            SectorPrograma.objects.create(sector_id=sector_id, programa_id=programa_instance.id)

        return programa_instance

    def update(self, instance, validated_data):
        sector_ids = validated_data.pop('sector_ids', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Actualizar los registros en SectorPrograma
        SectorPrograma.objects.filter(programa=instance).delete()
        for sector_id in sector_ids:
            SectorPrograma.objects.create(sector_id=sector_id, programa_id=instance.id)

        return instance


class TipoProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPrograma
        fields = ('__all__')

class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = ('__all__')

class ObjetivoProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoPrograma
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["objetivo_title"] = instance.objetivo.titulo
        return data