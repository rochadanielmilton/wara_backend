from rest_framework import serializers

from backend_mmaya.serializers import BaseCrudSerializer
from programas.serializers import ProgramasSerializer
from .models import *
from programas.models import SectoresClasificador,SubSectoresClasificador


class SubSectoresClasificadorSerializer(serializers.ModelSerializer):
    sector_clasificador_name = serializers.CharField(source='sector_clasificador.nombre', read_only=True)

    class Meta:
        model = SubSectoresClasificador
        fields = ['id', 'nombre', 'sector_clasificador', 'sector_clasificador_name', 'created_at', 'updated_at', 'is_deleted']

class SectoresClasificadorSerializer(serializers.ModelSerializer):
    sub_sectores = SubSectoresClasificadorSerializer(many=True, read_only=True)

    class Meta:
        model = SectoresClasificador
        fields = ['id', 'nombre', 'estado', 'created_at', 'updated_at', 'is_deleted', 'sub_sectores']
        
class DepartamentoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Departamento
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    departamento_id = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all(), source='departamento', write_only=True)
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Provincia
        fields = ('id', 'departamento_id', 'nombre','estado', 'created_at', 'updated_at', 'is_deleted')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['departamento'] = DepartamentoSerializer(instance.departamento).data if instance.departamento else None
        return data
    
class MunicipioSerializer(serializers.ModelSerializer):
    provincia_id = serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.all(), source='provincia', write_only=True)
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Provincia
        fields = ('id', 'provincia_id', 'nombre','estado', 'created_at', 'updated_at', 'is_deleted')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['provincia'] = ProvinciaSerializer(instance.provincia).data if instance.provincia else None
        return data
    
    def create(self, validated_data):
        provincia = validated_data.pop('provincia') 
        municipio = Municipio.objects.create(provincia=provincia, **validated_data)
        return municipio
    
class OrganizacionFinancieraSerializer(serializers.ModelSerializer):
    sigla = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = OrganizacionFinanciera
        fields = ('id', 'sigla', 'created_at', 'updated_at', 'is_deleted')

class EjecutorSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Ejecutor
        fields = ('id', 'estado', 'nombre', 'created_at', 'updated_at', 'is_deleted')

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoProyecto
        fields = ('id','nombre')

class MinisterioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    direccion = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    class Meta:
        model = Ministerio
        fields="__all__"

class ViceministerioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    direccion = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    ministerio_id = serializers.PrimaryKeyRelatedField(queryset=Ministerio.objects.all(), source='ministerio', write_only=True)
    descentralizadas_ids = serializers.PrimaryKeyRelatedField(queryset=Descentralizada.objects.filter(is_deleted=False), source="descentralizadas", write_only=True, many=True)
    class Meta:
        model = Viceministerio
        fields=("id","nombre","direccion","email","estado","ministerio_id","descentralizadas_ids")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ministerio'] = MinisterioSerializer(instance.ministerio).data if instance.ministerio else None
        data['descentralizadas'] = DescentralizadaSerializer(instance.descentralizadas.filter(is_deleted=False), many=True).data
        sectores = Sector.objects.filter(viceministeriosector__viceministerio=instance)
        data['sectores'] = SectorSerializer(sectores, many=True).data
        return data
    
    def create(self, validated_data):
        descentralizadas_data = validated_data.pop('descentralizadas')
        viceministerio = Viceministerio.objects.create(**validated_data)
        viceministerio.descentralizadas.set(descentralizadas_data)
        return viceministerio
    
    def update(self, instance, validated_data):
        descentralizadas_data = validated_data.pop('descentralizadas', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if descentralizadas_data is not None:
            instance.descentralizadas.set(descentralizadas_data)

        return instance
    
    

class DescentralizadaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    # direccion = serializers.CharField(max_length=255, required=True)
    # email = serializers.EmailField(max_length=255, required=True)
    class Meta:
        model = Ejecutor
        fields="__all__"

from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name'] # , 'created_at', 'updated_at', 'is_deleted']



class EmpresaConstructoraSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = EmpresaConstructora
        fields = ('id', 'nombre', 'estado', 'created_at', 'updated_at', 'is_deleted')

class SectorSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Sector
        fields = ('id', 'nombre', 'estado', 'created_at', 'updated_at', 'is_deleted')


class AgenciaFinanciadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model =AgenciaFinanciadora
        fields=('id','descripcion','sigla','estado', 'created_at', 'updated_at', 'is_deleted')

class UcepResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model= UcepResponsable
        fields=('id','nombre','estado','created_at','updated_at','is_deleted')

class TipoProyectoSerializer(BaseCrudSerializer):
    class Meta:
        model=TipoProyecto
        fields=('id','nombre','estado','created_at','updated_at','is_deleted')

class LugarSerializer(BaseCrudSerializer):
    class Meta:
        model=Lugar
        fields=('id','nombre','estado','created_at','updated_at','is_deleted')

class TipoFinanciamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model= TipoFinanciamiento
        fields=('id','nombre','estado','created_at','updated_at','is_deleted')

class EstadoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Estado2
        fields = '__all__'

class EstadoDetalladoSerializer(serializers.ModelSerializer):
    estado_proyecto = serializers.PrimaryKeyRelatedField(queryset=Estado2.objects.filter(is_deleted=False), write_only=True)
    class Meta:
        model = EstadoDetallado2
        fields = ('id', 'estado_proyecto', 'nombre', 'observacion', 'estado', 'created_at', 'updated_at', 'is_deleted')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['estado_proyecto'] = EstadoSerializer(instance.estado_proyecto).data
        return data
    
class CargoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Cargo
        fields = '__all__'

class ResposableContraparteSerializer(BaseCrudSerializer):
    class Meta:
        model = ResponsableContraparte
        fields = ('id', 'nombre', 'estado')

class CoEjecutoresSerializer(BaseCrudSerializer):
    class Meta:
        model = CoEjecutor
        fields = ('id', 'nombre', 'estado')

class SectorDetalladoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Sector
        fields=("id","nombre")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lugares'] = LugarSerializer(instance.lugares, many=True).data
        data['programas'] = ProgramasSerializer(instance.programas, many=True).data
        data['ejecutores'] = EjecutorSerializer(instance.ejecutores, many=True).data
        return data
    
class EstructuraOrganizativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstructuraOrganizativa
        fields = '__all__'