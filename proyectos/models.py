from django.db import models

class Conexion(models.Model):
    proyecto = models.OneToOneField('programas.Proyectos', models.DO_NOTHING, unique=True)
    agua_potable = models.IntegerField(null=True, blank=True)
    pileta_publica = models.IntegerField(null=True, blank=True)
    pozo_o_noria_con_bomba = models.IntegerField(null=True, blank=True)
    pozo_o_noria_protegido = models.IntegerField(null=True, blank=True)
    manantial_protegido = models.IntegerField(null=True, blank=True)
    recoleccion_de_agua_de_lluvia = models.IntegerField(null=True, blank=True)
    alcantarillado = models.IntegerField(null=True, blank=True)
    alcantarillado_condominial = models.IntegerField(null=True, blank=True)
    sistema_con_desague_a_camara_septica = models.IntegerField(null=True, blank=True)
    banos_con_arrastre_de_agua = models.IntegerField(null=True, blank=True)
    banos_secos_ecologicos = models.IntegerField(null=True, blank=True)
    letrina_con_descarga_a_pozo_de_absorcion = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'conexiones'
        verbose_name = 'Conexión'
        verbose_name_plural = 'Conexiones'

    def __str__(self):
        return f"Conexión {self.id}"
    
class Poblacion(models.Model):
    proyecto = models.ForeignKey('programas.Proyectos', on_delete=models.SET_NULL, null=True, blank=True)
    agua_potable = models.IntegerField(null=True, blank=True)
    pileta_publica = models.IntegerField(null=True, blank=True)
    pozo_o_noria_con_bomba = models.IntegerField(null=True, blank=True)
    pozo_o_noria_protegido = models.IntegerField(null=True, blank=True)
    manantial_protegido = models.IntegerField(null=True, blank=True)
    recoleccion_de_agua_de_lluvia = models.IntegerField(null=True, blank=True)
    alcantarillado = models.IntegerField(null=True, blank=True)
    alcantarillado_condominial = models.IntegerField(null=True, blank=True)
    sistema_con_desague_a_camara_septica = models.IntegerField(null=True, blank=True)
    banos_con_arrastre_de_agua = models.IntegerField(null=True, blank=True)
    banos_secos_ecologicos = models.IntegerField(null=True, blank=True)
    letrina_con_descarga_a_pozo_de_absorcion = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'poblaciones'
        verbose_name_plural = 'Poblaciones'

class DrenajePluvial(models.Model):
    proyecto = models.ForeignKey('programas.Proyectos', models.DO_NOTHING, blank=True, null=True)
    familias_beneficiadas = models.IntegerField(blank=True, null=True)
    poblacion_beneficiada = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'drenajes_pluviales'
        verbose_name_plural = 'Drenajes Pluviales'

class VariableImpacto(models.Model):
    proyecto = models.ForeignKey('programas.Proyectos', models.DO_NOTHING, blank=True, null=True)
    area_intervencion_km2 = models.IntegerField(blank=True, null=True)
    hectareas_forestadas = models.IntegerField(blank=True, null=True)
    hectareas_reforestadas = models.IntegerField(blank=True, null=True)
    viveros_construccion_forta = models.IntegerField(blank=True, null=True)
    superficie_protegida = models.CharField(max_length=100, blank=True, null=True)
    informacion = models.CharField(max_length=50, blank=True, null=True)
    hectareas_protegidas = models.IntegerField(blank=True, null=True)
    sistemas_riego = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'variables_impacto'