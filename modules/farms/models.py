from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.core.models import TimeStampedModel

class Farm(TimeStampedModel):
    name = models.CharField(_("Nombre"), max_length=120)
    location = models.CharField(_("Ubicación"), max_length=150)
    description = models.TextField(_("Descripción"), blank=True)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Granja")
        verbose_name_plural = _("Granjas")
        ordering = ["name"]

    def __str__(self):
        return self.name

class Zone(TimeStampedModel):
    class IrrigationMode(models.TextChoices):
        MANUAL = "MANUAL", _("Manual")
        AUTOMATIC = "AUTOMATIC", _("Automático")
        SCHEDULED = "SCHEDULED", _("Programado")

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="zones", verbose_name=_("Granja"))
    name = models.CharField(_("Nombre"), max_length=100)
    code = models.SlugField(_("Código"), max_length=50, unique=True)
    crop_name = models.CharField(_("Nombre del cultivo"), max_length=100, blank=True)
    area_m2 = models.DecimalField(_("Área (m2)"), max_digits=10, decimal_places=2, default=0)
    irrigation_mode = models.CharField(
        _("Modo de riego"),
        max_length=20,
        choices=IrrigationMode.choices,
        default=IrrigationMode.AUTOMATIC,
    )
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Zona")
        verbose_name_plural = _("Zonas")
        ordering = ["farm__name", "name"]

    def __str__(self):
        return f"{self.farm.name} - {self.name}"
