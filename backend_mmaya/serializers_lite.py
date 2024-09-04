from rest_framework import serializers

from backend_mmaya.serializers import BaseCrudSerializer
from parametros.serializers import ViceministerioSerializer
from programas.serializers import ProgramasSerializer,Programas
from parametros.models import *
from proyectos_preinversion.models import ProyectosPreinversion
class DepartamentoSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Departamento
        fields = ('id','nombre')

class ProvinciaSelectSerializer(serializers.ModelSerializer):
    departamento_id = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all(), source='departamento', write_only=True)
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Provincia
        fields = ('id', 'departamento_id', 'nombre')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['departamento'] = DepartamentoSelectSerializer(instance.departamento).data if instance.departamento else None
        return data
    
class MunicipioSelectSerializer(serializers.ModelSerializer):
    provincia_id = serializers.PrimaryKeyRelatedField(queryset=Provincia.objects.all(), source='provincia', write_only=True)
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Provincia
        fields = ('id', 'provincia_id', 'nombre')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['provincia'] = ProvinciaSelectSerializer(instance.provincia).data if instance.provincia else None
        return data
    
    def create(self, validated_data):
        provincia = validated_data.pop('provincia') 
        municipio = Municipio.objects.create(provincia=provincia, **validated_data)
        return municipio
class ProgramasSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Programas
        fields=('id','sigla_prog_convenio') 
          
class OrganizacionFinancieraSelectSerializer(serializers.ModelSerializer):
    sigla = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = OrganizacionFinanciera
        fields = ('id', 'sigla')

class EjecutorSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Ejecutor
        fields = ('id','nombre')

class EstadoSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoProyecto
        fields = ('id','nombre')

class MinisterioSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ministerio
        fields = ('id','nombre')
class ViceministerioSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    ministerio_id = serializers.PrimaryKeyRelatedField(queryset=Ministerio.objects.all(), source='ministerio', write_only=True)
    descentralizadas_ids = serializers.PrimaryKeyRelatedField(queryset=Descentralizada.objects.filter(is_deleted=False), source="descentralizadas", write_only=True, many=True)
    class Meta:
        model = Viceministerio
        fields=("id","nombre","ministerio_id","descentralizadas_ids")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['ministerio'] = MinisterioSelectSerializer(instance.ministerio).data if instance.ministerio else None
        data['descentralizadas'] = DescentralizadaSelectSerializer(instance.descentralizadas.filter(is_deleted=False), many=True).data
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
    
    

class DescentralizadaSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    # direccion = serializers.CharField(max_length=255, required=True)
    # email = serializers.EmailField(max_length=255, required=True)
    class Meta:
        model = Ejecutor
        fields= ('id', 'name')

from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')



class EmpresaConstructoraSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = EmpresaConstructora
        fields = ('id', 'nombre')

class SectorSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    viceministerio = ViceministerioSelectSerializer(read_only=True, source='viceministerio_set.first')
    class Meta:
        model = Sector
        fields = ('id', 'nombre','viceministerio')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class AgenciaFinanciadoraSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model =AgenciaFinanciadora
        fields=('id','descripcion','sigla')

class UcepResponsableSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model= UcepResponsable
        fields=('id','nombre')

class TipoProyectoSelectSerializer(BaseCrudSerializer):
    class Meta:
        model=TipoProyecto
        fields=('id','nombre')

class LugarSelectSerializer(BaseCrudSerializer):
    class Meta:
        model=Lugar
        fields=('id','nombre')

class TipoFinanciamientoSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model= TipoFinanciamiento
        fields=('id','nombre')

class EstadoSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Estado2
        fields = ('id','nombre')
class EstadoDetalladoSelectSerializer(serializers.ModelSerializer):
    estado_proyecto = serializers.PrimaryKeyRelatedField(queryset=Estado2.objects.filter(is_deleted=False), write_only=True)
    class Meta:
        model = EstadoDetallado2
        fields = ('id', 'estado_proyecto', 'nombre')


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['estado_proyecto'] = EstadoSelectSerializer(instance.estado_proyecto).data
        return data
    
class CargoSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Cargo
        fields = ('id', 'nombre')

class ResposableContraparteSelectSerializer(BaseCrudSerializer):
    class Meta:
        model = ResponsableContraparte
        fields = ('id', 'nombre')

class CoEjecutoresSelectSerializer(BaseCrudSerializer):
    class Meta:
        model = CoEjecutor
        fields = ('id', 'nombre')

class SectorDetalladoSelectSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Sector
        fields=("id","nombre")
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lugares'] = LugarSelectSerializer(instance.lugares, many=True).data
        data['programas'] = ProgramasSerializer(instance.programas, many=True).data
        data['ejecutores'] = EjecutorSelectSerializer(instance.ejecutores, many=True).data
        return data
    
class PreinversionSelectSerializer(BaseCrudSerializer):
    class Meta:
        model = ProyectosPreinversion
        fields = ('id', 'codigo_convenio')