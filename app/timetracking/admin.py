import csv

from typing import Any, Callable, Sequence, Union
from django import forms
from django.contrib import admin, messages
from django.db.models import Model, QuerySet, TextChoices
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import URLPattern, path
from django.utils.translation import gettext_lazy as _

from . import models


class ExportForm(forms.Form):
    class OutputChoice(TextChoices):
        CSV = "csv", _("CSV")

    output = forms.ChoiceField(
        label=_("Output"), choices=OutputChoice.choices, initial=OutputChoice.CSV
    )

    required_css_class = "required"


class EventAdmin(admin.ModelAdmin):
    ordering = ("-date",)
    date_hierarchy = "date"
    search_fields = (
        "employee__username",
        "employee__first_name",
        "employee__last_name",
        "project__name",
    )

    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return request.user.is_superuser

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(employee=request.user)
        return qs

    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        list_display = ["date", "project", "duration"]
        if request.user.is_superuser:
            list_display.insert(1, "employee")
        return list_display

    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        list_filter = ["project"]
        if request.user.is_superuser:
            list_filter.append("employee")
        return list_filter

    def get_fields(
        self, request: HttpRequest, obj: Model | None = ...
    ) -> Sequence[Union[Callable[..., Any], str]]:
        fields = ["date", "project", "duration", "comments"]
        if request.user.is_superuser:
            fields.insert(1, "employee")
        return fields

    def save_model(self, request: Any, obj: Model, form: Any, change: Any) -> None:
        obj.employee = request.user
        return super().save_model(request, obj, form, change)

    def get_urls(self) -> list[URLPattern]:
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        custom_urls = [
            path(
                "export/",
                self.admin_site.admin_view(self.export),
                name="%s_%s_export" % info,
            ),
        ]
        return custom_urls + urls

    def export(self, request: HttpRequest, extra_context: Any = None) -> HttpResponse:
        if not request.user.is_superuser:
            self.message_user(
                request,
                _("You are not authorized to access this page"),
                level=messages.ERROR,
            )
            return redirect("..")

        if request.method == "POST":
            form = ExportForm(request.POST)
            if form.is_valid():
                rows = models.Event.objects.all()
                fieldnames = [field.name for field in models.Event._meta.fields]

                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = "attachment; filename=events.csv"

                output = form.cleaned_data["output"]
                if output == ExportForm.OutputChoice.CSV:
                    writer = csv.DictWriter(response, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in rows:
                        data = {field: str(getattr(row, field)) for field in fieldnames}
                        writer.writerow(data)
                else:
                    message = _(
                        "Error while exporting data: unsupported output format %(format)s"
                    ) % {"format": str(output)}
                    level = messages.ERROR
                    self.message_user(
                        request,
                        message,
                        level=level,
                    )
                    response = redirect("..")

                return response
        else:
            form = ExportForm()

        context = {
            **self.admin_site.each_context(request),
            "title": _("Export"),
            "description": _("Export data to selected output format"),
            "opts": self.model._meta,
            "form": form,
            **(extra_context or {}),
        }

        return render(
            request,
            "admin/timetracking/event/export.html",
            context,
        )


class ProjectAdmin(admin.ModelAdmin):
    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser


class ProjectDurationPerMonthViewAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "project", "total_duration")
    list_display_links = None
    list_filter = ("year", "month", "project")
    ordering = ("-year", "-month")
    sortable_by = ("year", "month", "project", "total_duration")

    def has_module_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser

    def has_view_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return request.user.is_superuser

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Model | None = None
    ) -> bool:
        return False


admin.site.register(models.Project, admin.ModelAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(
    models.ProjectDurationPerMonthView, ProjectDurationPerMonthViewAdmin
)
