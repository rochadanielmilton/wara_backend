from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path,include
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Seguimiento de Proyectos - WARA",
        default_version='v1',
        description="Sistema de Seguimiento de Proyectos del Ministerio de Medio Ambiente y agua",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sistemas@tu_api.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

selective_schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Seguimiento de Proyectos - WARA",
        default_version='v1',
        description="Sistema de Seguimiento de Proyectos del Ministerio de Medio Ambiente y agua",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sistemas@tu_api.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/', include('programas.urls_v2')),
        path('api/', include('logs.urls')),
        path('o/', include('external.urls')),
    ],
)

project_schema_view = get_schema_view(
    openapi.Info(
        title="Sistema de Seguimiento de Proyectos - WARA",
        default_version='v1',
        description="Sistema de Seguimiento de Proyectos del Ministerio de Medio Ambiente y agua",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sistemas@tu_api.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/', include('proyectos.urls')),
        path('api/', include('logs.urls')),
        path('o/', include('external.urls')),
    ],
)


urlpatterns = [
    path('o/', include('external.urls', namespace='external')),
    path('admin/', admin.site.urls),
    path('media/', include('django.contrib.staticfiles.urls')),
    path('api/auth/',include('authentication.urls')),
    path('api/',include('parametros.urls_v2')),
    path('api/',include('administracion.urls_v2')),
    path('api/reportes/',include('reportes.urls_v2')),
    path('programas/',include('programas.urls')),
    path('api/',include('programas.urls_v2')),
    path('api/',include('proyectos.urls')),
    path('api/',include('logs.urls')),
    path('api/',include('proyectos_preinversion.urls')),
    path('api/',include('backend_mmaya.urls_lite')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        re_path(r'^swagger-programas(?P<format>\.json|\.yaml)$', selective_schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger-programas/', selective_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-programas'),
        path('redoc-programas/', selective_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-programas'),
        path('swagger-proyectos/', project_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-proyectos'),
        path('redoc-proyectos/', project_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-proyectos'),
    ]