from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TemplatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.templates"
    verbose_name = _("Templates")
