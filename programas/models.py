from django.db import models
from backend_mmaya.models import BaseCrudModel
from parametros.enums import Estados
from parametros.models import Programa, Viceministerio
#from proyectos_preinversion.models import ProyectosPreinversion
from administracion.models import AuthUser
class Sectores(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'sectores'
    def __str__(self):
        return self.nombre if self.nombre else f"Sectores ID: {self.id}"
class Lugares(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    created_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(AuthUser, models.DO_NOTHING, related_name='lugares_updated_by_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lugares'
    def __str__(self):
        return self.nombre if self.nombre else f"Lugares ID: {self.id}"
    
class OrganizacionesFinancieras(models.Model):
    sigla = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'organizaciones_financieras'
    def __str__(self):
        return self.sigla if self.sigla else f"OrganizacionesFinancieras ID: {self.id}"
class Ejecutores(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'ejecutores'
    def __str__(self):
        return self.nombre if self.nombre else f"Ejecutores ID: {self.id}"
class Estados2(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    estado = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados2'

class EstadosDetallados2(models.Model):
    estado = models.ForeignKey(Estados2, models.DO_NOTHING, blank=True, null=True)
    nombre = models.CharField(max_length=255)
    observacion = models.TextField(blank=True, null=True)
    estado_field = models.TextField(db_column='estado')  # Field renamed because of name conflict. This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados_detallados2'
        unique_together = (('estado', 'nombre'),)

from django.db import models
from django.contrib.auth.models import User

class Programas(models.Model):
    codigo_convenio = models.CharField(max_length=100,blank=True, null=True)
    viceministerio = models.TextField(blank=True, null=True)
    entidad_ejecutora = models.TextField(blank=True, null=True)
    co_ejecutor = models.TextField(blank=True, null=True)
    programas_proyectos = models.TextField(blank=True, null=True)
    sigla_prog_convenio = models.TextField(blank=True, null=True)
    agencia_financiadora = models.TextField(blank=True, null=True)
    descripcion_agencia_financiadora = models.TextField(blank=True, null=True)
    tipo_convenio = models.TextField(blank=True, null=True)
    documento_respaldo = models.TextField(blank=True, null=True)
    enlace_convenio = models.TextField(blank=True, null=True)
    tipo_financiamiento = models.TextField(blank=True, null=True)
    departamentos_field = models.TextField(db_column='departamentos_', blank=True, null=True)  # Field renamed because it ended with '_'.
    municpios = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    subsector = models.TextField(blank=True, null=True)
    fecha_suscripcion_convenio_contrato = models.TextField(blank=True, null=True)
    fecha_vencimiento = models.TextField(blank=True, null=True)
    nueva_fecha_vencimiento = models.TextField(blank=True, null=True)
    hoy = models.TextField(blank=True, null=True)
    vigente_no_vigente = models.TextField(blank=True, null=True)
    estructura_financiera = models.TextField(blank=True, null=True)
    enlace_estructura_financiera = models.TextField(blank=True, null=True)
    componentes_field = models.TextField(db_column='componentes_', blank=True, null=True)  # Field renamed because it ended with '_'.
    enlace_componentes = models.TextField(blank=True, null=True)
    desembolsos = models.TextField(blank=True, null=True)
    enlace_desembolsos = models.TextField(blank=True, null=True)
    ejecucion_programa_fuente_externa = models.TextField(blank=True, null=True)
    enlace_ejecucion_del_programa_fuente_externa = models.TextField(blank=True, null=True)
    ejecucion_del_programa_contraparte_local = models.TextField(blank=True, null=True)
    enlace_ejecucion_del_programa_contraparte_local = models.TextField(blank=True, null=True)
    proyectos_inversion = models.TextField(blank=True, null=True)
    enlace_proyectos_inversion = models.TextField(blank=True, null=True)
    proyectos_preinversion = models.TextField(blank=True, null=True)
    enlace_proyectos_preinversion = models.TextField(blank=True, null=True)
    superficies_bajo_riego_ha = models.TextField(blank=True, null=True)
    enlace_superficies_bajo_riego_ha = models.TextField(blank=True, null=True)
    manejo_integral_cuencas_km2 = models.TextField(blank=True, null=True)
    n_ptap = models.TextField(blank=True, null=True)
    n_ptar = models.TextField(blank=True, null=True)
    n_habitantes_con_acceso_a_saneamiento_basico = models.TextField(blank=True, null=True)
    otros = models.TextField(blank=True, null=True)
    enlace_otros = models.TextField(blank=True, null=True)
    indicadores_programa_psdi_pdes = models.TextField(blank=True, null=True)
    estado_situacion_programa_field = models.TextField(db_column='estado_situacion_programa_', blank=True, null=True)  # Field renamed because it ended with '_'.
    detallado_descripcion = models.TextField(blank=True, null=True)
    detallado_codigo = models.CharField(max_length=255, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    created_by_id = models.IntegerField(blank=True, null=True)
    updated_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programas'

    def __str__(self):
        return self.sigla_prog_convenio if self.sigla_prog_convenio else (self.programas_proyectos if self.programas_proyectos else f"Programa ID: {self.id}")

class EmpresasConstructoras(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'empresas_constructoras'
    def __str__(self):
        return self.nombre if self.nombre else f"EmpresasConstructoras ID: {self.id}"

class Proyectos(models.Model):
    codigo_convenio = models.CharField(max_length=100,blank=True, null=True)
    lugar = models.ForeignKey(Lugares, models.DO_NOTHING, blank=True, null=True)
    sector = models.ForeignKey('Sectores', models.DO_NOTHING, blank=True, null=True)
    preinversion = models.ForeignKey('proyectos_preinversion.ProyectosPreinversion', models.DO_NOTHING, blank=True, null=True)
    nombre = models.CharField(max_length=1255, blank=True, null=True)
    organizacion = models.ForeignKey(OrganizacionesFinancieras, models.DO_NOTHING, blank=True, null=True)
    ejecutor = models.ForeignKey(Ejecutores, models.DO_NOTHING, blank=True, null=True)
    tipo = models.ForeignKey('TiposProyecto', models.DO_NOTHING, blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    estado_detallado = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_conclusion = models.DateField(blank=True, null=True)
    programa = models.ForeignKey(Programas, models.DO_NOTHING, blank=True, null=True)
    poblacion_beneficiaria_cuencas = models.CharField(max_length=100, blank=True, null=True)
    numero_familias_beneficiadas = models.IntegerField(blank=True, null=True,default=0)
    numero_familias_indirectas = models.IntegerField(blank=True, null=True,default=0)
    toneladas_residuos_dispuestos_anio = models.FloatField(blank=True, null=True)
    toneladas_residuos_aprovechamiento_anio = models.FloatField(blank=True, null=True)
    superficie_riego_ha = models.FloatField(blank=True, null=True)
    hectareas_bajo_riego = models.IntegerField(blank=True, null=True)
    hectareas_reforestadas = models.IntegerField(blank=True, null=True)
    sistemas_riego = models.FloatField(blank=True, null=True)
    numero_plantines = models.IntegerField(blank=True, null=True)
    forestacion_ha = models.IntegerField(blank=True, null=True)
    reforestacion_ha = models.IntegerField(blank=True, null=True)
    superficie_plantada = models.IntegerField(blank=True, null=True)
    viveros = models.IntegerField(blank=True, null=True)
    empleos_directos = models.IntegerField(blank=True, null=True,default=0)
    empleos_indirectos = models.IntegerField(blank=True, null=True,default=0)
    empresa_constructora = models.ForeignKey(EmpresasConstructoras, models.DO_NOTHING, blank=True, null=True)
    proyecto_cuenta_con_ptar = models.CharField(max_length=50, blank=True, null=True)
    proyectos_con_sin_represa = models.CharField(max_length=50, blank=True, null=True)
    ucep_responsable = models.ForeignKey('UcepResponsables', models.DO_NOTHING, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    tipo_proyecto_detallado = models.CharField(max_length=700, blank=True, null=True)
    conclusion = models.DateField(blank=True, null=True)
    gobierno = models.CharField(max_length=50, blank=True, null=True)
    obs_fechaini_fechafin = models.CharField(db_column='obs_fechaIni_fechaFin', max_length=255, blank=True, null=True)  # Field name made lowercase.
    obs_avance = models.CharField(max_length=255, blank=True, null=True)
    obs_poblacion_beneficiara = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_inicio_cif = models.DateField(blank=True, null=True)
    fecha_fin_cif = models.DateField(blank=True, null=True)
    beneficiados_varones = models.IntegerField(blank=True, null=True, default=0)
    beneficiados_mujeres = models.IntegerField(blank=True, null=True, default=0)
    total_programado_2024 = models.FloatField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    programado_para_entrega_por_efemeride = models.TextField(blank=True, null=True)
    estado_reportado_por_el_sector_para_efemeride = models.TextField(blank=True, null=True)
    viceministerio = models.ForeignKey(Viceministerio, models.DO_NOTHING, blank=True, null=True)
    emblematico = models.BooleanField(blank=True, null=True,default='f')
    gestion = models.IntegerField(blank=True, null=True)
    estado_detallado_nuevo = models.ForeignKey(EstadosDetallados2, models.DO_NOTHING, blank=True, null=True)
    estado = models.ForeignKey(Estados2, models.DO_NOTHING, blank=True, null=True)
    tipo_conflicto = models.CharField(max_length=255,blank=True,null=True)
    descripcion_conflicto = models.CharField(max_length=255,blank=True,null=True)
    tipo_migrado = models.CharField(max_length=255, default='nuevo')
    codigo_sisin = models.CharField(max_length=50)
    latitud = models.CharField(max_length=100, blank=True, null=True)
    longitud = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    documento_creacion = models.FileField(upload_to='proyectos/documentos/', blank=True, null=True)
    imagen_proyecto =  models.ImageField(upload_to='proyectos/imagen/',max_length=255, default='defecto.jpg', null=True, blank=True)
    sector_clasificador = models.ForeignKey('SectoresClasificador', models.DO_NOTHING, blank=True, null=True)
    sub_sector_clasificador = models.ForeignKey('SubSectoresClasificador', models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'proyectos'

class Seguimiento(models.Model):
    id = models.SmallAutoField(primary_key=True)
    realizacion = models.ForeignKey('Realizaciones', models.DO_NOTHING, blank=True, null=True)
    proyecto_id = models.SmallIntegerField(blank=True, null=True)
    mes = models.CharField(max_length=20, blank=True, null=True)
    anio = models.CharField(max_length=20, blank=True, null=True)
    total_programado_proyecto = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    avance_financiero_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    porcentaje_avance_financiero_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    porcentaje_resto_financiero_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    porcentaje_avance_fisico_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    porcentaje_resto_fisico_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    fotografia_1 = models.ImageField(upload_to='seguimientos/imagen/',max_length=255, blank=True, null=True)
    fotografia_2 = models.ImageField(upload_to='seguimientos/imagen/',max_length=255, blank=True, null=True)
    fotografia_3 = models.ImageField(upload_to='seguimientos/imagen/',max_length=255, blank=True, null=True)
    fotografia_4 = models.ImageField(upload_to='seguimientos/imagen/',max_length=255, blank=True, null=True)
    documento_respaldo_avance = models.FileField(upload_to='seguimientos/documentos/', blank=True, null=True)
    fecha_actualizacion_avance = models.DateTimeField(auto_now=True)
    detalle_seguimiento = models.TextField(blank=True, null=True)
    acumulado_financiero_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    acumulado_porcentaje_financiero_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    acumulado_porcentaje_fisico_mes = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    estado_proyecto = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_id = models.IntegerField(blank=True, null=True)
    update_by_id = models.IntegerField(blank=True, null=True)
    saldo_programado_proyecto = models.DecimalField(max_digits=16, decimal_places=2,blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    estado_seguimiento = models.CharField(max_length=30,default='pendiente')
    observacion_estado = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'seguimiento'

class SectoresClasificador(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    estado = models.TextField(default='HABILITADO')  # This field type is a guess.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'sectores_clasificador'
    def sub_sectores(self):
        return SubSectoresClasificador.objects.filter(sector_clasificador=self, is_deleted=False)
class SubSectoresClasificador(models.Model):
    nombre = models.CharField(unique=True, max_length=255)
    sector_clasificador = models.ForeignKey(SectoresClasificador, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'sub_sectores_clasificador'
class TiposProyecto(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tipos_proyecto'
    def __str__(self):
        return self.nombre if self.nombre else f"Departamento ID: {self.id}"
class UcepResponsables(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'ucep_responsables'
    def __str__(self):
        return self.nombre if self.nombre else f"Departamento ID: {self.id}"
class Departamentos(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'departamentos'
    def __str__(self):
        return self.nombre if self.nombre else f"Departamento ID: {self.id}"
    
class Provincias(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'provincias'
    def __str__(self):
        return self.nombre if self.nombre else f"Provincia ID: {self.id}"

class Municipios(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.ForeignKey(Provincias, models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'municipios'

    def __str__(self):
        return self.nombre if self.nombre else f"Municipio ID: {self.id}"

class Realizaciones(models.Model):
    proyecto = models.OneToOneField(Proyectos, models.DO_NOTHING, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, blank=True, null=True)
    provincia = models.ForeignKey(Provincias, models.DO_NOTHING, blank=True, null=True)
    municipio = models.ForeignKey(Municipios, models.DO_NOTHING, blank=True, null=True)
    estado = models.ForeignKey(Estados2, models.DO_NOTHING, blank=True, null=True)
    total_inversion = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    avance_fisico = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,default=0)
    avance_financiamiento = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True,default=0)
    inversion_presupuestada = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    saldo_presupuesto = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    fecha_concl_obra = models.DateField(blank=True, null=True)
    conclusion_concl_proy = models.DateField(blank=True, null=True)
    contraparte_local = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    contraparte_local_no_financiera = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    contratado = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    eje_acum = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    proyecto_cuenta_con_ptar = models.CharField(max_length=50, blank=True, null=True,default=0)
    financiamiento_externo = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    gad = models.FloatField(blank=True, null=True,default=0)
    gad_no_financiero = models.FloatField(blank=True, null=True,default=0)
    presupuesto_vapsb = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True,default=0)
    total_ejecutado_acumulado_bs_2023 = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    total_ejecutado_mill_bs_2023 = models.IntegerField(blank=True, null=True)
    total_inversion_mill = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    responsable_contraparte = models.ForeignKey('ResponsablesContraparte', models.DO_NOTHING, blank=True, null=True)
    ejecutor = models.ForeignKey(Ejecutores, models.DO_NOTHING, blank=True, null=True)
    org_financ = models.ForeignKey(OrganizacionesFinancieras, models.DO_NOTHING, blank=True, null=True)
    programa = models.ForeignKey(Programas, models.DO_NOTHING, blank=True, null=True)
    tipo_de_proyecto = models.ForeignKey(TiposProyecto, models.DO_NOTHING, blank=True, null=True)
    ucep_responsable = models.ForeignKey('UcepResponsables', models.DO_NOTHING, blank=True, null=True)
    lugar = models.ForeignKey(Lugares, models.DO_NOTHING, blank=True, null=True)
    bol = models.DecimalField(max_digits=16, decimal_places=2,blank=True, null=True,default=0)
    ppcr = models.DecimalField(max_digits=16, decimal_places=2,blank=True, null=True,default=0)
    financiamiento_pnc = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    departamentos = models.ManyToManyField(
        Departamentos,
        related_name="departamentos_realizacion",
        blank=True,
        through='RealizacionDepartamentos'
    )
    provincias = models.ManyToManyField(
        Provincias,
        related_name="provincias_realizacion",
        blank=True,
        through='RealizacionProvincias'
    )
    municipios = models.ManyToManyField(
        Municipios,
        related_name="municipios_realizacion",
        blank=True,
        through='RealizacionMunicipios'
    )

    class Meta:
        managed = False
        db_table = 'realizaciones'

class RealizacionDepartamentos(models.Model):
    realizacion = models.ForeignKey(Realizaciones, models.DO_NOTHING, blank=True, null=True)
    departamento = models.ForeignKey(Departamentos, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realizacion_departamentos'


class RealizacionMunicipios(models.Model):
    realizacion = models.ForeignKey(Realizaciones, models.DO_NOTHING, blank=True, null=True)
    municipio = models.ForeignKey(Municipios, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realizacion_municipios'


class RealizacionProvincias(models.Model):
    realizacion = models.ForeignKey(Realizaciones, models.DO_NOTHING, blank=True, null=True)
    provincia = models.ForeignKey(Provincias, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realizacion_provincias'


class ResponsablesContraparte(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'responsables_contraparte'

class TipoPrograma(BaseCrudModel):
    nombre = models.CharField(max_length=255, unique=True)
    estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)

    class Meta:
        db_table = 'tipos_programa'
        verbose_name_plural = 'tipos de programas'

    def __str__(self):
        return self.nombre if self.nombre else f'Tipo de Programa {self.id}'
    
class Objetivo(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    # estado = models.CharField(choices=[(status.value, status.value) for status in Estados], default=Estados.HABILITADO.value)

    class Meta:
        db_table = 'objetivos'
        verbose_name_plural = 'objetivos'

    def __str__(self):
        return self.titulo
    
class ObjetivoPrograma(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    objetivo = models.ForeignKey(Objetivo, on_delete=models.CASCADE)
    valor = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = (('programa', 'objetivo'),)
        db_table = 'objetivo_programa'
        verbose_name_plural = 'tabla pivot de objetivos con programas'

    def __str__(self):
        return f"{self.programa} - {self.objetivo}"