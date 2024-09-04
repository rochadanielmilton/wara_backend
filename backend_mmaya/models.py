from backend_mmaya.managers import NonDeletedManager
from django.db import models

class BaseCrudModel(models.Model):
    is_deleted = models.BooleanField(default=False, null=True)
    created_by = models.ForeignKey('authentication.CustomUser', related_name='created_%(class)s', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey('authentication.CustomUser', related_name='updated_%(class)s', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NonDeletedManager()  
    all_objects = models.Manager() 

    class Meta:
        abstract = True

class BaseCrudNoCreatedByUpdatedByModel(models.Model):
    is_deleted = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NonDeletedManager()  
    all_objects = models.Manager() 

    class Meta:
        abstract = True