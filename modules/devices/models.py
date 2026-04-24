from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.core.models import TimeStampedModel
from modules.farms.models import Zone

class Device(TimeStampedModel):
    class DeviceType(models.TextChoices):
        CONTROLLER = "CONTROLLER", _("Controlador")
        GATEWAY = "GATEWAY", _("Gateway")

    class Status(models.TextChoices):
        ONLINE = "ONLINE", _("En línea")
        OFFLINE = "OFFLINE", _("Desconectado")
        MAINTENANCE = "MAINTENANCE", _("Mantenimiento")

    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
        verbose_name=_("Zona")
    )
    device_id = models.CharField(_("ID del Dispositivo"), max_length=50, unique=True)
    name = models.CharField(_("Nombre"), max_length=100)
    device_type = models.CharField(
        _("Tipo de dispositivo"),
        max_length=20,
        choices=DeviceType.choices,
        default=DeviceType.CONTROLLER,
    )
    firmware_version = models.CharField(_("Versión de firmware"), max_length=50, blank=True)
    ip_address = models.GenericIPAddressField(_("Dirección IP"), null=True, blank=True)
    mac_address = models.CharField(_("Dirección MAC"), max_length=50, blank=True)
    status = models.CharField(
        _("Estado"),
        max_length=20,
        choices=Status.choices,
        default=Status.OFFLINE,
    )
    last_seen = models.DateTimeField(_("Última vez visto"), null=True, blank=True)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Dispositivo")
        verbose_name_plural = _("Dispositivos")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.device_id})"

class Sensor(TimeStampedModel):
    class SensorType(models.TextChoices):
        SOIL_MOISTURE = "SOIL_MOISTURE", _("Humedad de suelo")
        TEMPERATURE = "TEMPERATURE", _("Temperatura")
        HUMIDITY = "HUMIDITY", _("Humedad ambiental")
        FLOW = "FLOW", _("Caudal")
        PRESSURE = "PRESSURE", _("Presión")
        RAIN = "RAIN", _("Lluvia")

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sensors", verbose_name=_("Dispositivo"))
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="sensors", verbose_name=_("Zona"))
    name = models.CharField(_("Nombre"), max_length=100)
    sensor_type = models.CharField(_("Tipo de sensor"), max_length=30, choices=SensorType.choices)
    unit = models.CharField(_("Unidad"), max_length=20)
    pin = models.CharField(_("Pin"), max_length=20, blank=True)
    min_value = models.DecimalField(_("Valor mínimo"), max_digits=10, decimal_places=2, null=True, blank=True)
    max_value = models.DecimalField(_("Valor máximo"), max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensores")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.get_sensor_type_display()}"

class Actuator(TimeStampedModel):
    class ActuatorType(models.TextChoices):
        PUMP = "PUMP", _("Bomba")
        VALVE = "VALVE", _("Válvula")
        RELAY = "RELAY", _("Relé")

    class State(models.TextChoices):
        OFF = "OFF", _("Apagado")
        ON = "ON", _("Encendido")
        OPEN = "OPEN", _("Abierto")
        CLOSED = "CLOSED", _("Cerrado")

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="actuators", verbose_name=_("Dispositivo"))
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="actuators", verbose_name=_("Zona"))
    name = models.CharField(_("Nombre"), max_length=100)
    actuator_type = models.CharField(_("Tipo de actuador"), max_length=20, choices=ActuatorType.choices)
    pin = models.CharField(_("Pin"), max_length=20, blank=True)
    state = models.CharField(_("Estado"), max_length=20, choices=State.choices, default=State.OFF)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Actuador")
        verbose_name_plural = _("Actuadores")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.get_actuator_type_display()}"
