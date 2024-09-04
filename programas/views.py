from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets,filters
from backend_mmaya.views import SoftDeleteModelViewSet
from logs.models import UserAction
from programas.mixin import MultipleFieldLookupMixin
from proyectos.serializers import ProyectosSerializer
from proyectos_preinversion.models import ProyectosPreinversion
from .models import *
from .serializers import ObjetivoProgramaSerializer, ObjetivoSerializer, ProgramasSerializer, TipoProgramaSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404, HttpResponse,JsonResponse
from django.template.loader import get_template
from django.utils.timezone import now
from xhtml2pdf import pisa
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
class ProgramaSerializerViewSet(SoftDeleteModelViewSet):
    queryset = Programas.objects.all().prefetch_related('sectorprograma_set__sector','sectorprograma_set','proyectos_set')
    serializer_class = ProgramasSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['viceministerio','sigla_prog_convenio','programas_proyectos']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@api_view(['GET'])
def reporte_programas_pdf(request):
    programa_id = request.GET.get('programa_id')

    if not programa_id:
        return JsonResponse({'message': 'No se proporcionó el ID del programa'}, status=400)

    try:
        programa_instance = Programas.objects.get(id=programa_id)
    except Programas.DoesNotExist:
        return JsonResponse({'message':'El registro no se encuentra'},status=404)
        
    template_path = 'reporte-programa.html'
    base_url = f"{request.scheme}://{request.get_host()}"
    context = {
        'usuario':request.user,
        'base_url': base_url,
        'current_datetime':now(),
        'programa_instance':programa_instance
    }
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF: {}'.format(pisa_status.err))

    return response

class TipoProgramaSerializerViewSet(SoftDeleteModelViewSet):
    queryset = TipoPrograma.objects.all()
    serializer_class = TipoProgramaSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['nombre']

class ObjetivoViewSet(viewsets.ModelViewSet):
    queryset = Objetivo.objects.all()
    serializer_class = ObjetivoSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['titulo']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['titulo']

class ObjetivoProgramaListView(generics.ListAPIView):
    serializer_class = ObjetivoProgramaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        programa_id = self.kwargs['programa_id']
        return ObjetivoPrograma.objects.filter(programa_id=programa_id).prefetch_related('objetivo')

class ObjetivoProgramaDetailView(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = ObjetivoPrograma.objects.all()
    serializer_class = ObjetivoProgramaSerializer
    multiple_lookup_fields = ['programa_id', 'objetivo_id']
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        UserAction.log_action(
            user=request.user,
            action_name="Eliminar",
            instance=instance
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            instance = None

        programa_id = kwargs.get('programa_id')
        objetivo_id = kwargs.get('objetivo_id')
        programa = get_object_or_404(Programa, id=programa_id)
        objetivo = get_object_or_404(Objetivo, id=objetivo_id)
        data = request.data.copy()
        data['programa'] = programa.id
        data['objetivo'] = objetivo.id

        if instance:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            UserAction.log_action(
                user=request.user,
                action_name="Actualizar",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            UserAction.log_action(
                user=request.user,
                action_name="Crear",
                instance=self.queryset.get(pk=serializer.data['id'])
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def numero_proyectos_por_programa_pdf(request):
    template_path = 'reporte-proyectos-por-programa.html'
    base_url = f"{request.scheme}://{request.get_host()}"

    programa_id = request.GET.get('programa_id', None)
    queryset = Proyectos.objects.filter(is_deleted=False, programa_id=programa_id,estado_id=3)

    context = {
        'usuario':request.user,
        'programa':Programas.objects.get(id=programa_id).sigla_prog_convenio,
        'base_url': base_url,
        'current_datetime': now(),
        'proyectos': queryset,
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proyectos.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Failed to generate PDF: {pisa_status.err}', status=500)

    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def numero_preinversion_por_programa_pdf(request):
    template_path = 'reporte-preinversion-por-programa.html'
    base_url = f"{request.scheme}://{request.get_host()}"

    programa_id = request.GET.get('programa_id', None)
    queryset = ProyectosPreinversion.objects.filter(is_deleted=False, programa_id=programa_id)

    context = {
        'usuario':request.user,
        'programa':Programas.objects.get(id=programa_id).sigla_prog_convenio,
        'base_url': base_url,
        'current_datetime': now(),
        'proyectos_preinversion': queryset,
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="proyectos.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'Failed to generate PDF: {pisa_status.err}', status=500)

    return response

