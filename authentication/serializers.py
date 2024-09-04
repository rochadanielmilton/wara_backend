from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from authentication.models import CustomUser, Menu,MenuPadre

from django.contrib.auth.models import Group

from parametros.serializers import CargoSerializer, DescentralizadaSerializer, SectorSerializer, ViceministerioSerializer

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
class MenuPadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuPadre
        fields = ('id', 'nombre_menu','icono')

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    menu_padre = serializers.SerializerMethodField()
    cargo = serializers.SerializerMethodField()
    viceministerio = serializers.SerializerMethodField()
    descentralizada = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return GroupSerializer(obj.groups, many=True).data
    
    def get_permissions(self, obj):
        return PermissionSerializer(obj.permissions, many=True).data
    
    def get_menu_padre(self, obj):
        menu_padres = MenuPadre.objects.filter(
            menu__in=obj.menus.filter(is_deleted=False)
        ).order_by('id').distinct()
        return MenuPadreSerializer(menu_padres, many=True).data
    
    def get_cargo(self, obj):
        return CargoSerializer(obj.cargo).data if obj.cargo is not None else None
    def get_viceministerio(self, obj):
        return ViceministerioSerializer(obj.viceministerio).data if obj.viceministerio is not None else None
    def get_descentralizada(self, obj):
        return DescentralizadaSerializer(obj.descentralizada).data if obj.descentralizada is not None else None
    def get_sector(self, obj):
        return SectorSerializer(obj.sector).data if obj.sector is not None else None
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'second_last_name'
                  ,'groups'
                  ,'permissions'
                  ,'menu_padre'
                  ,'cargo','viceministerio','descentralizada','sector')
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["menu"] = MenuSerializer(instance.menus, many=True).data
        return data
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
