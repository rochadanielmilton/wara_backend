from rest_framework import serializers
from programas.models import Sectores, Proyectos

class SectoresSerializer(serializers.ModelSerializer):
     class Meta:
        model = Sectores
        fields = '__all__'

class ProyectoSerializer(serializers.ModelSerializer):
     class Meta:
        model = Proyectos
        fields = '__all__'
