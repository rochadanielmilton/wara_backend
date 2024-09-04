from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

class Action(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'actions'
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

    def __str__(self):
        return self.nombre

class UserAction(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    resource = models.CharField(max_length=255)
    extra = models.CharField(max_length=255, null=True, blank=True)
    resource_affected = models.JSONField(encoder=DjangoJSONEncoder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_actions'
        verbose_name = 'User Action'
        verbose_name_plural = 'User Actions'

    def __str__(self):
        return f"{self.user} - {self.action}"

    @classmethod
    def log_action(cls, user, action_name, instance,extra=None):
        model_name = instance._meta.model_name  
        action = Action.objects.get(nombre=action_name)
        resource_affected_json = serialize('json', [instance])

        cls.objects.create(
            user=user,
            action=action,
            resource=model_name,
            resource_affected=resource_affected_json,
            extra=extra
        )