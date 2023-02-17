from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TimeTrackingConfig(AppConfig):
    name = "app.timetracking"
    verbose_name = _("Time Tracking")
