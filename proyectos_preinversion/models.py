from django.db import models
from parametros.models import AuthUser,Departamento,Provincia,Municipio,Ejecutor,OrganizacionFinanciera,Programa
from programas.models import Viceministerio,TiposProyecto,UcepResponsables,Programas

class TiposProyectoPreinversion(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    estado = models.TextField(default='HABILITADO')  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default='f')
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='tiposproyectopreinversion_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_proyecto_preinversion'

class EstadosPreinversion(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    estado = models.TextField(default='HABILITADO')  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default='f')
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='estadospreinversion_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados_preinversion'
        
class Comunidades(models.Model):
    nombre = models.CharField(unique=True, max_length=760)
    municipio = models.ForeignKey(Municipio, models.DO_NOTHING)
    estado = models.TextField(default='HABILITADO')  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default='f')
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='comunidades_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comunidades'

class ProyectosPreinversion(models.Model):
    codigo_sisin = models.CharField(max_length=16, blank=True, null=True)
    codigo_convenio = models.CharField(max_length=100,blank=True, null=True)
    sector = models.CharField(max_length=50)
    sub_sector = models.CharField(max_length=50)
    tipo_proyecto = models.ForeignKey(TiposProyecto, models.DO_NOTHING)
    departamento = models.ForeignKey(Departamento, models.DO_NOTHING)
    provincia = models.ForeignKey(Provincia, models.DO_NOTHING, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, models.DO_NOTHING, blank=True, null=True)
    ucep_responsable = models.ForeignKey(UcepResponsables, models.DO_NOTHING, blank=True, null=True)
    ejecutor = models.ForeignKey(Ejecutor, models.DO_NOTHING)
    programa = models.ForeignKey(Programas, models.DO_NOTHING, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    monto_comprometido_estudio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monto_contratado_estudio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monto_pagado_estudio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avance_financiero = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_conclusion = models.DateField(blank=True, null=True)
    estado_preinversion = models.ForeignKey(EstadosPreinversion, models.DO_NOTHING, db_column='estado_id')
    observacion = models.CharField(max_length=255, blank=True, null=True)
    viceministerio = models.ForeignKey(Viceministerio, models.DO_NOTHING, blank=True, null=True)
    estado = models.TextField(default='HABILITADO')  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default='f')
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='proyectospreinversion_updated_by_set', blank=True, null=True)
    comunidades = models.ManyToManyField(Comunidades,through="PreinversionComunidad", related_name="comunidades")
    organismos_financiadores = models.ManyToManyField(OrganizacionFinanciera,through="PreinversionOrganismoFinanciador", related_name="organismos_financiadores")
    class Meta:
        managed = False
        db_table = 'proyectos_preinversion'

class PreinversionComunidad(models.Model):
    preinversion = models.ForeignKey(ProyectosPreinversion, models.DO_NOTHING)
    comunidad = models.ForeignKey(Comunidades, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'preinversion_comunidad'
        unique_together = (('preinversion', 'comunidad'),)

class PreinversionOrganismoFinanciador(models.Model):
    preinversion = models.ForeignKey(ProyectosPreinversion, models.DO_NOTHING)
    organismo_financiador = models.ForeignKey(OrganizacionFinanciera, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'preinversion_organismo_financiador'
        unique_together = (('preinversion', 'organismo_financiador'),)

class Meta(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'metas'
        verbose_name_plural = 'metas'

    def __str__(self):
        return self.titulo
    
class MetaPreinversion(models.Model):
    preinversion = models.ForeignKey(ProyectosPreinversion, on_delete=models.CASCADE)
    meta = models.ForeignKey(Meta, on_delete=models.CASCADE)
    valor = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = (('preinversion', 'meta'),)
        db_table = 'meta_preinversion'
        verbose_name_plural = 'tabla pivot de metas con proyectos de preinversión'

    def __str__(self):
        return f"{self.preinversion} - {self.meta}"