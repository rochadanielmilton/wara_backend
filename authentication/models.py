from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.models import ContentType

from administracion.models import AuthGroup, AuthPermission,AuthUser
from parametros.enums import Estados
from parametros.models import Cargo, Descentralizada, Ejecutor, Sector, Viceministerio
from programas.models import Ejecutores



class Menu(models.Model):
    ruta = models.CharField(max_length=255)
    icono = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    grupo = models.CharField(max_length=255)
    groups = models.ManyToManyField(AuthGroup,through="GroupMenu", related_name="menus")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    orden = models.IntegerField(default=1)
    menu_padre = models.ForeignKey('MenuPadre', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'menu'

class MenuPadre(models.Model):
    nombre_menu = models.CharField(max_length=100, blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_padre'

class CustomUser(AbstractUser):
    DESCENTRALIZADA = 'DESCENTRALIZADA'
    MINISTERIO = 'MINISTERIO'
    VICEMINISTERIO = 'VICEMINISTERIO'
    SECTOR = 'SECTOR'

    TIPO_CHOICES = [
        (DESCENTRALIZADA, 'Descentralizada'),
        (MINISTERIO, 'Ministerio'),
        (VICEMINISTERIO, 'Viceministerio'),
        (SECTOR, 'Sector'),
    ]

    second_last_name=models.CharField(max_length=150, blank=True, null=True)
    groups = models.ManyToManyField(AuthGroup,through='UserGroup')
    permissions = models.ManyToManyField(AuthPermission,through='UserPermission')
    menus = models.ManyToManyField(Menu,through="UserMenu")
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    viceministerio = models.ForeignKey(Viceministerio, models.DO_NOTHING, blank=True, null=True)
    descentralizada = models.ForeignKey(Ejecutores, models.DO_NOTHING, blank=True, null=True)
    cargo = models.ForeignKey(Cargo,models.DO_NOTHING, blank=True, null=True)
    sector = models.ForeignKey(Sector,models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey('CustomUser',models.SET_NULL, blank=True, null=True, related_name='created_by_user')
    updated_by = models.ForeignKey('CustomUser',models.SET_NULL, blank=True, null=True, related_name='updated_by_user')
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_CHOICES,
        default=MINISTERIO,
    )

    def is_viceministerio(self):
        return self.tipo == self.VICEMINISTERIO
    
    def is_ministerio(self):
        return self.tipo == self.MINISTERIO
    
    def is_descentralizada(self):
        return self.tipo == self.DESCENTRALIZADA

    def is_sector(self):
        return self.tipo == self.SECTOR
    
    def has_group(self, group_names):
        if isinstance(group_names, str):
            group_names = [group_names]
        return self.groups.filter(name__in=group_names).exists()
    
    class Meta:
        db_table = 'auth_user'

class UserGroup(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="user_id")
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE, db_column="group_id")
    class Meta:
        db_table = 'auth_user_groups'
    
class UserPermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="user_id")
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE, db_column="permission_id")
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class GroupMenu(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    class Meta:
        db_table = 'group_menu'

class UserMenu(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="user_id")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column="menu_id")
    class Meta:
        managed = False
        db_table = 'user_menu'

