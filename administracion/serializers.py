from rest_framework import serializers
from django.contrib.auth.models import Group as AuthGroup, Permission,User
from authentication.models import*
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermission
        fields = ('id', 'name', 'codename', 'content_type_id', 'created_at', 'updated_at', 'is_deleted')

    def create(self, validated_data):
        validated_data['content_type_id'] = 1  
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['content_type_id'] = 1  
        return super().update(instance, validated_data)

class AuthGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthGroup
        fields = ('id','name')

from django.contrib.auth.hashers import make_password
class AuthUserSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(choices=[('MINISTERIO', 'MINISTERIO'), ('SECTOR', 'SECTOR')])
    cargo_id = serializers.PrimaryKeyRelatedField(
        queryset=Cargo.objects.filter(is_deleted=False), source='cargo', write_only=True,required=False, allow_null=True
    )
    viceministerio_id = serializers.PrimaryKeyRelatedField(
        queryset=Viceministerio.objects.filter(is_deleted=False), source='viceministerio', write_only=True, required=False, allow_null=True
    )
    descentralizada_id = serializers.PrimaryKeyRelatedField(
        queryset=Descentralizada.objects.filter(is_deleted=False), source='descentralizada', write_only=True, required=False, allow_null=True
    )
    group_id = serializers.PrimaryKeyRelatedField(
        queryset=AuthGroup.objects.filter(is_deleted=False), source='group', write_only=True
    )
    menus_ids = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.filter(is_deleted=False), source="menus", write_only=True, many=True
    )
    permissions_ids = serializers.PrimaryKeyRelatedField(
        queryset=AuthPermission.objects.filter(is_deleted=False), source="permissions", write_only=True, many=True
    )
    sector_id = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects.filter(is_deleted=False), source='sector', write_only=True,required=False, allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = (
            'id', 'password', 'username', 'first_name', 'last_name', 'email', 'second_last_name', 
            'group_id', 'menus_ids', 'permissions_ids', 'estado', 'cargo_id', 
            'viceministerio_id', 'descentralizada_id', 'created_by_id', 'updated_by_id',
            'tipo','sector_id'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("password", None)
        data['groups'] = [group.name for group in instance.groups.all()] 
        return data
    
    def validate(self, attrs):
        tipo = attrs.get('tipo')
        viceministerio = attrs.get('viceministerio',None)
        sector = attrs.get('sector',None)
        
        if tipo == 'SECTOR' and (not viceministerio or not sector):
            raise serializers.ValidationError("Viceministerio y Sector son requeridos")

        return attrs

    def create(self, validated_data):
        created_by = self.context['request'].user
        instance = CustomUser.objects.create(**validated_data, created_by=created_by)
        return instance

class UpdateAuthUserSerializer(AuthUserSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        updated_by = self.context['request'].user
        instance.updated_by = updated_by
        group_instance = validated_data.pop('group')
        menus_ids = validated_data.pop('menus')
        permissions_ids = validated_data.pop('permissions')

        menus = Menu.objects.filter(id__in=[menu.id for menu in menus_ids])
        permissions = AuthPermission.objects.filter(id__in=[perm.id for perm in permissions_ids])

        combined_menus = list(set(menus)) 
        combined_permissions = list(set(permissions))

        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.groups.clear()
        instance.groups.add(group_instance)

        instance.menus.clear()
        instance.menus.set(combined_menus)
        instance.permissions.clear()
        instance.permissions.set(combined_permissions)

        return instance



class DjandoContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'

class AuthUserUserPermissionsReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    permission = serializers.CharField(source='permission.name')

    class Meta:
        model = AuthUserUserPermissions
        fields = ['id', 'user', 'permission']

class AuthUserUserPermissionsCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all(), source='user')
    permission_id = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), source='permission')

    class Meta:
        model = AuthUserUserPermissions
        fields = ['id', 'user_id', 'permission_id']


class AuthGroupPermissionsReadSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    permission = serializers.CharField(source='permission.name')

    class Meta:
        model = AuthGroupPermissions
        fields = ['id', 'group', 'permission']
class AuthGroupPermissionsCreateSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=AuthGroup.objects.all(), source='group')
    permission_id = serializers.PrimaryKeyRelatedField(queryset=AuthPermission.objects.all(), source='permission')

    class Meta:
        model = AuthGroupPermissions
        fields = ['id', 'group_id', 'permission_id']

class AuthUserGroupsReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    group = serializers.CharField(source='group.name')

    class Meta:
        model = AuthUserGroups
        fields = ['id', 'user', 'group']
class AuthUserGroupsCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all(), source='user')
    group_id = serializers.PrimaryKeyRelatedField(queryset=AuthGroup.objects.all(), source='group')

    class Meta:
        model = AuthUserGroups
        fields = ['id', 'user_id', 'group_id']
CustomUser = get_user_model()
class UserMenuReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    menu = serializers.CharField(source='menu.nombre')

    class Meta:
        model = UserMenu
        fields = ['id', 'user', 'menu']

class UserMenuCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    menu_id = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), source='menu')

    class Meta:
        model = UserMenu
        fields = ['id', 'user_id', 'menu_id']
        
# class ProgramaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Programa
#         fields = ('id', 'sigla','detallado_descripcion', 'detallado_codigo', 'estado', 'created_at', 'updated_at', 'is_deleted',)

class GroupMenuSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source='group.id', read_only=True)
    grupo = serializers.SlugRelatedField(slug_field='name', queryset=AuthGroup.objects.all(), source='group')
    menu_id = serializers.IntegerField(source='menu.id', read_only=True)
    menu = serializers.SlugRelatedField(slug_field='nombre', queryset=Menu.objects.all())
    
    class Meta:
        model = GroupMenu
        fields = ['id', 'group_id', 'grupo', 'menu_id', 'menu']

class GroupMenuCreateSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=AuthGroup.objects.all(), source='group')
    menu_ids = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all(), many=True, source='menu')

    class Meta:
        model = GroupMenu
        fields = ['id', 'group_id', 'menu_ids']

class GroupMenuDeleteSerializer(serializers.Serializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=AuthGroup.objects.all(), source='group')
    menu = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all()))




        