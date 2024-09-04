from django.db import models
from django.db.models import Q

class NonDeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class PermissionNonDeletedManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        queryset = queryset.filter(
            ~Q(content_type_id__in=[5, 6, 10, 11, 12, 13, 14]) & 
            ~Q(name__icontains='log entry')
        )
        return queryset