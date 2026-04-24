from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from modules.core.models import TimeStampedModel
from modules.farms.models import Zone
from modules.devices.models import Device, Sensor, Actuator

class IrrigationRule(TimeStampedModel):
    class Action(models.TextChoices):
        TURN_ON = "TURN_ON", _("Encender")
        OPEN = "OPEN", _("Abrir")

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="rules", verbose_name=_("Zona"))
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="rules",
        limit_choices_to={"sensor_type": Sensor.SensorType.SOIL_MOISTURE},
        verbose_name=_("Sensor")
    )
    actuator = models.ForeignKey(Actuator, on_delete=models.CASCADE, related_name="rules", verbose_name=_("Actuador"))
    name = models.CharField(_("Nombre"), max_length=120)
    min_threshold = models.DecimalField(_("Umbral mínimo"), max_digits=10, decimal_places=2)
    action = models.CharField(_("Acción"), max_length=20, choices=Action.choices, default=Action.TURN_ON)
    duration_minutes = models.PositiveIntegerField(_("Duración (minutos)"), default=10)
    cooldown_minutes = models.PositiveIntegerField(_("Tiempo de espera (minutos)"), default=15)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Regla de riego")
        verbose_name_plural = _("Reglas de riego")
        ordering = ["zone__name", "name"]

    def __str__(self):
        return self.name

class IrrigationSchedule(TimeStampedModel):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="schedules", verbose_name=_("Zona"))
    actuator = models.ForeignKey(Actuator, on_delete=models.CASCADE, related_name="schedules", verbose_name=_("Actuador"))
    name = models.CharField(_("Nombre"), max_length=120)
    days_of_week = models.CharField(
        _("Días de la semana"),
        max_length=50,
        help_text=_("Ejemplo: MON,TUE,WED")
    )
    start_time = models.TimeField(_("Hora de inicio"))
    duration_minutes = models.PositiveIntegerField(_("Duración (minutos)"), default=10)
    active = models.BooleanField(_("Activo"), default=True)

    class Meta:
        verbose_name = _("Programación de riego")
        verbose_name_plural = _("Programaciones de riego")
        ordering = ["zone__name", "start_time"]

    def __str__(self):
        return self.name

class SensorReading(TimeStampedModel):
    class Quality(models.TextChoices):
        GOOD = "GOOD", _("Buena")
        ESTIMATED = "ESTIMATED", _("Estimada")
        BAD = "BAD", _("Mala")

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="readings", verbose_name=_("Sensor"))
    value = models.DecimalField(_("Valor"), max_digits=10, decimal_places=2)
    quality = models.CharField(_("Calidad"), max_length=20, choices=Quality.choices, default=Quality.GOOD)
    timestamp = models.DateTimeField(_("Fecha y hora"), default=timezone.now)
    raw_payload = models.JSONField(_("Payload crudo"), default=dict, blank=True)

    class Meta:
        verbose_name = _("Lectura de sensor")
        verbose_name_plural = _("Lecturas de sensores")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sensor.name} - {self.value} ({self.timestamp})"

class Command(TimeStampedModel):
    class CommandType(models.TextChoices):
        TURN_ON = "TURN_ON", _("Encender")
        TURN_OFF = "TURN_OFF", _("Apagar")
        OPEN = "OPEN", _("Abrir")
        CLOSE = "CLOSE", _("Cerrar")
        SET_AUTO = "SET_AUTO", _("Modo automático")
        SET_MANUAL = "SET_MANUAL", _("Modo manual")

    class Source(models.TextChoices):
        RULE = "RULE", _("Regla")
        SCHEDULE = "SCHEDULE", _("Programación")
        MANUAL = "MANUAL", _("Manual")
        API = "API", _("API")

    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pendiente")
        SENT = "SENT", _("Enviado")
        EXECUTED = "EXECUTED", _("Ejecutado")
        FAILED = "FAILED", _("Fallido")
        CANCELED = "CANCELED", _("Cancelado")

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="commands", verbose_name=_("Zona"))
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="commands", verbose_name=_("Dispositivo"))
    actuator = models.ForeignKey(Actuator, on_delete=models.CASCADE, related_name="commands", verbose_name=_("Actuador"))
    rule = models.ForeignKey(IrrigationRule, on_delete=models.SET_NULL, null=True, blank=True, related_name="commands", verbose_name=_("Regla"))
    schedule = models.ForeignKey(IrrigationSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name="commands", verbose_name=_("Programación"))
    command = models.CharField(_("Comando"), max_length=20, choices=CommandType.choices)
    source = models.CharField(_("Origen"), max_length=20, choices=Source.choices, default=Source.MANUAL)
    status = models.CharField(_("Estado"), max_length=20, choices=Status.choices, default=Status.PENDING)
    desired_duration_minutes = models.PositiveIntegerField(_("Duración deseada (minutos)"), null=True, blank=True)
    payload = models.JSONField(_("Payload"), default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="irrigation_commands",
        verbose_name=_("Creado por")
    )
    sent_at = models.DateTimeField(_("Enviado el"), null=True, blank=True)
    executed_at = models.DateTimeField(_("Ejecutado el"), null=True, blank=True)

    class Meta:
        verbose_name = _("Comando")
        verbose_name_plural = _("Comandos")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.device.device_id} - {self.command} - {self.status}"

class IrrigationLog(TimeStampedModel):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="logs", verbose_name=_("Zona"))
    actuator = models.ForeignKey(Actuator, on_delete=models.CASCADE, related_name="logs", verbose_name=_("Actuador"))
    command = models.ForeignKey(Command, on_delete=models.SET_NULL, null=True, blank=True, related_name="logs", verbose_name=_("Comando"))
    start_time = models.DateTimeField(_("Hora de inicio"), default=timezone.now)
    end_time = models.DateTimeField(_("Hora de fin"), null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(_("Duración real (minutos)"), null=True, blank=True)
    water_volume_liters = models.DecimalField(_("Volumen de agua (litros)"), max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Historial de riego")
        verbose_name_plural = _("Historial de riego")
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.zone.name} - {self.start_time}"

class Alert(TimeStampedModel):
    class AlertType(models.TextChoices):
        LOW_MOISTURE = "LOW_MOISTURE", _("Humedad baja")
        DEVICE_OFFLINE = "DEVICE_OFFLINE", _("Dispositivo desconectado")
        SENSOR_ERROR = "SENSOR_ERROR", _("Error de sensor")
        EXECUTION_FAILURE = "EXECUTION_FAILURE", _("Fallo de ejecución")
        MAINTENANCE = "MAINTENANCE", _("Mantenimiento")

    class Severity(models.TextChoices):
        LOW = "LOW", _("Baja")
        MEDIUM = "MEDIUM", _("Media")
        HIGH = "HIGH", _("Alta")
        CRITICAL = "CRITICAL", _("Crítica")

    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts", verbose_name=_("Zona"))
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts", verbose_name=_("Dispositivo"))
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts", verbose_name=_("Sensor"))
    actuator = models.ForeignKey(Actuator, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts", verbose_name=_("Actuador"))
    command = models.ForeignKey(Command, on_delete=models.SET_NULL, null=True, blank=True, related_name="alerts", verbose_name=_("Comando"))
    alert_type = models.CharField(_("Tipo de alerta"), max_length=30, choices=AlertType.choices)
    severity = models.CharField(_("Severidad"), max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    title = models.CharField(_("Título"), max_length=150)
    message = models.TextField(_("Mensaje"))
    acknowledged = models.BooleanField(_("Reconocida"), default=False)
    acknowledged_at = models.DateTimeField(_("Reconocida el"), null=True, blank=True)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acknowledged_irrigation_alerts",
        verbose_name=_("Reconocida por")
    )

    class Meta:
        verbose_name = _("Alerta")
        verbose_name_plural = _("Alertas")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
