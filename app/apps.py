from django.contrib.admin.apps import AdminConfig


class AppAdminConfig(AdminConfig):
    default_site = "app.admin.AppAdminSite"
