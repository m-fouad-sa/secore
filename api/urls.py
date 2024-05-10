from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        contact=openapi.Contact(email="m.fouad.sa@outlook.com"),
        license=openapi.License(name="Secure License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/common/", include("core_apps.common.urls")),
]

admin.site.site_header = "Secure Backend Admin Site"
admin.site.site_title = "Secure Backend Portal"
admin.site.index_title = "Welcome to the Secure Portal"
