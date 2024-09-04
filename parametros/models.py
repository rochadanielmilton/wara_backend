from django.db import models
from administracion.models import AuthUser
from django.utils import timezone
from administracion.models import Departamento
from backend_mmaya.managers import NonDeletedManager
from backend_mmaya.models import BaseCrudModel, BaseCrudNoCreatedByUpdatedByModel
from .enums import Estados

class Provincia(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=False)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'provincias'

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=False)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    provincia = models.ForeignKey(Provincia,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'municipios'

    def __str__(self):
        return self.nombre
    
class EstadoProyecto(models.Model):
    nombre = models.CharField(max_length=255, null=False, blank=False)
    estado = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        db_table = 'estados2'
        verbose_name_plural = 'estados_proyecto'

    def __str__(self):
        return self.nombre if self.nombre else f'EstadoProyecto {self.id}'
    

class Lugar(BaseCrudModel):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)

    class Meta:
        db_table = 'lugares'
        verbose_name_plural = 'lugares'

    def __str__(self):
        return self.nombre if self.nombre else f'Lugar {self.id}'

class Sector(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    lugares = models.ManyToManyField(
        Lugar,
        verbose_name="lugares",
        blank=True,
        through='SectorLugar'
    )
    programas = models.ManyToManyField(
        'programas.Programas',
        related_name="programas_sector",
        verbose_name="programas",
        blank=True,
        through='SectorPrograma'
    )
    ejecutores = models.ManyToManyField(
        'Ejecutor',
        verbose_name="permissions",
        blank=True,
        through='SectorEjecutor'
    )

    class Meta:
        managed = False
        db_table = 'sectores'
        verbose_name_plural = 'sectores'

    def __str__(self):
        return self.nombre if self.nombre else f'Sector {self.id}'



class OrganizacionFinanciera(models.Model):
    sigla = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'organizaciones_financieras'
        verbose_name_plural = 'organizaciones_financieras'
        ordering = ['id']

    def __str__(self):
        return self.nombre 

class Ejecutor(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'ejecutores'
        verbose_name_plural = 'ejecutores'

    def __str__(self):
        return self.nombre if self.nombre else f'Ejecutor {self.id}'


class TipoProyecto(BaseCrudModel):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)

    class Meta:
        db_table = 'tipos_proyecto'
        verbose_name_plural = 'tipos_proyecto'

    def __str__(self):
        return self.nombre if self.nombre else f'Tipo de Proyecto {self.id}'

class Programa(models.Model):
    sigla = models.CharField(max_length=255, null=True, blank=True, db_column="sigla_prog_convenio")

    class Meta:
        db_table = 'programas'
        verbose_name_plural = 'programas'

    def __str__(self):
        return self.sigla if self.sigla else f'Programa {self.id}'


class EmpresaConstructora(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'empresas_constructoras'
        verbose_name_plural = 'empresas_constructoras'

    def __str__(self):
        return self.nombre if self.nombre else f'EmpresaConstructora {self.id}'


class UcepResponsable(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, default='HABILITADO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'ucep_responsables'
        verbose_name_plural = 'ucep_responsables'

    def __str__(self):
        return self.nombre if self.nombre else f'UcepResponsable {self.id}'
    
class AgenciaFinanciadora(models.Model):
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    sigla = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, default='HABILITADO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'agencia_financiadora'

class TipoFinanciamiento(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, default='HABILITADO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tipo_financiamiento'
    
    def __str__(self):
        return self.nombre if self.nombre else f'TipoFinanciamiento {self.id}'

class Ministerio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        db_table = 'ministerios'
        unique_together= ('nombre',)
        ordering = ['id']

    def __str__(self):
	    return self.nombre


class Descentralizada(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'descentralizadas'
        unique_together = ('nombre',)
        ordering = ['id']

    def __str__(self):
        return self.nombre
class Viceministerio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    ministerio = models.ForeignKey(Ministerio, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    descentralizadas = models.ManyToManyField(Descentralizada,through='ViceministerioDescentralizada', verbose_name="descentralizadas",)
    sectores = models.ManyToManyField(Sector,through='ViceministerioSector',verbose_name="sectores",)

    class Meta:
        db_table = 'viceministerios'
        unique_together = ('nombre',)
        ordering = ['id']

    def __str__(self):
        return self.nombre
class ViceministerioDescentralizada(models.Model):
    viceministerio = models.ForeignKey(Viceministerio, on_delete=models.CASCADE, db_column="viceministerio_id")
    descentralizada = models.ForeignKey(Descentralizada, on_delete=models.CASCADE,db_column="descentralizada_id")

    class Meta:
        db_table = 'viceministerio_descentralizada'
        unique_together = (('viceministerio', 'descentralizada'),)
        ordering = ['viceministerio_id', 'descentralizada_id']

    def __str__(self):
        return f"{self.viceministerio.nombre} - {self.descentralizada.nombre}"

class ViceministerioSector(models.Model):
    viceministerio = models.ForeignKey(Viceministerio, on_delete=models.CASCADE, db_column="viceministerio_id")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,db_column="sector_id")

    class Meta:
        managed = False
        db_table = 'viceministerio_sector'
        unique_together = (('viceministerio', 'sector'),)   

class Estado2(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    tipo = models.CharField(max_length=255, default="nuevo")

    class Meta:
        managed = False
        db_table = 'estados2'
        unique_together = ('nombre',)
        ordering = ['id']

    def __str__(self):
        return self.nombre
    
class EstadoDetallado2(models.Model):
    estado_proyecto = models.ForeignKey(Estado2, on_delete=models.CASCADE,db_column="estado_id")
    nombre = models.CharField(max_length=255)
    observacion = models.TextField(blank=True, null=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value, db_column="estado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'estados_detallados2'
        unique_together = ('nombre','estado_proyecto')
        ordering = ['id']

    def __str__(self):
        return self.nombre

class ResponsableContraparte(BaseCrudModel):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    class Meta:
        db_table = 'responsables_contraparte'

    def __str__(self):
        return self.nombre if self.nombre else f'Responsable Contraparte {self.id}'
    
class CoEjecutor(BaseCrudModel):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    class Meta:
        db_table = 'co_ejecutores'

    def __str__(self):
        return self.nombre if self.nombre else f'Coejecutores {self.id}'
    
class SectorLugar(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)

    class Meta:
        managed=False
        db_table = 'sector_lugar' 

class SectorPrograma(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    programa = models.ForeignKey('programas.Programas', on_delete=models.CASCADE)
    
    class Meta:
        managed=False
        db_table = 'sector_programa'

class SectorEjecutor(models.Model):
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    ejecutor = models.ForeignKey(Ejecutor, on_delete=models.CASCADE)
    class Meta:
        managed=False
        db_table = 'sector_ejecutor' 

class Area(BaseCrudModel):
    nombre = models.CharField(unique=True, max_length=255)
    estado = models.TextField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)  
    ministerio = models.ForeignKey('Ministerio', on_delete=models.CASCADE)
   
    class Meta:
        managed = False
        db_table = 'areas'

class EstructuraOrganizativa(BaseCrudModel):
    nombre = models.CharField(unique=True, max_length=255)
    estado = models.TextField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)  
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    class Meta:
        managed = False
        db_table = 'estructuras_organizativas'

class Cargo(BaseCrudNoCreatedByUpdatedByModel):
    nombre = models.CharField(max_length=255)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)
    estructura_organizativa = models.ForeignKey(EstructuraOrganizativa, models.CASCADE)
    denominacion_cargo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cargos'