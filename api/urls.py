from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      contact=openapi.Contact(email="m.fouad.sa@outlook.com"),
      license=openapi.License(name="SECORE License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   #path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path(settings.ADMIN_URL, admin.site.urls),
    
]

admin.site.site_header = "API Admin"
admin.site.site_title = "API Admin Portal"
admin.site.index_title = "Welcome to the API Portal"
