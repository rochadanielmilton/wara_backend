from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import User, Permission
#from authentication.models import Menu

from backend_mmaya.managers import PermissionNonDeletedManager
from parametros.enums import Estados

# Modelo AuthPermission en la aplicación administracion
class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, models.DO_NOTHING, related_name='administracion_authpermissions')
    codename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = PermissionNonDeletedManager()  
    all_objects = models.Manager() 

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    permissions = models.ManyToManyField(
        AuthPermission,
        verbose_name="permissions",
        blank=True,
        through='GroupPermission'
    )

    class Meta:
        managed = False
        db_table = 'auth_group'

class GroupPermission(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)
    class Meta:
        managed=False
        db_table = 'auth_group_permissions'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    second_last_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'

class Departamento(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = f"departamentos"
        ordering = ['id']

    def __str__(self):
        return self.nombre 
class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class Programa(models.Model):
    sigla = models.CharField(max_length=255)
    detallado_descripcion = models.TextField(null=True, blank=True)
    detallado_codigo = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed=False
        db_table = 'programas'
        verbose_name_plural = "programas"
        unique_together = (('sigla'),)

