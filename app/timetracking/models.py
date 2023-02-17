from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    id = models.BigAutoField(verbose_name=_("id"), primary_key=True)
    name = models.CharField(
        verbose_name=_("name"), max_length=255, unique=True, null=False, blank=False
    )

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    id = models.BigAutoField(verbose_name=_("id"), primary_key=True)
    date = models.DateField(verbose_name=_("date"))
    duration = models.DurationField(verbose_name=_("duration"))
    comments = models.TextField(verbose_name=_("comments"), blank=True)
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("employee"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.date} - {self.employee} - {self.project} - {self.duration}"


class ProjectDurationPerMonthView(models.Model):
    class Meta:
        managed = False

    id = models.BigAutoField(verbose_name=_("id"), primary_key=True)
    year = models.CharField(verbose_name=_("year"), max_length=4)
    month = models.CharField(verbose_name=_("month"), max_length=2)
    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )
    total_duration = models.DurationField(verbose_name=_("total duration"))
