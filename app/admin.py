from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AppAdminSite(admin.AdminSite):
    site_title = _("Jean-Jean Corp Internal Management Tool")
    site_header = _("Jean-Jean Corp")
    index_title = _("Internal Management Tool")
