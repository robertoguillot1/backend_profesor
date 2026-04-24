from datetime import timedelta
from django.utils import timezone
from modules.devices.models import Device, Actuator, Sensor
from .models import IrrigationRule, SensorReading, Command, Alert, IrrigationLog

def mark_device_online(device: Device):
    device.status = Device.Status.ONLINE
    device.last_seen = timezone.now()
    device.save()

def apply_command_to_actuator(command: Command):
    actuator = command.actuator
    now = timezone.now()

    if command.command in [Command.CommandType.TURN_ON, Command.CommandType.OPEN]:
        # Cambiar estado del hardware
        actuator.state = Actuator.State.ON if command.command == Command.CommandType.TURN_ON else Actuator.State.OPEN
        actuator.save()
        
        # Iniciar registro en el historial
        IrrigationLog.objects.create(
            zone=command.zone,
            actuator=actuator,
            command=command,
            start_time=now
        )

    elif command.command in [Command.CommandType.TURN_OFF, Command.CommandType.CLOSE]:
        # Cambiar estado del hardware
        actuator.state = Actuator.State.OFF if command.command == Command.CommandType.TURN_OFF else Actuator.State.CLOSED
        actuator.save()
        
        # Cerrar el último registro abierto para este actuador
        last_log = IrrigationLog.objects.filter(
            actuator=actuator, 
            end_time__isnull=True
        ).order_by('-start_time').first()
        
        if last_log:
            last_log.end_time = now
            duration = now - last_log.start_time
            last_log.duration_minutes = int(duration.total_seconds() / 60)
            last_log.save()

def evaluate_reading_and_generate_automation(reading: SensorReading):
    sensor = reading.sensor
    zone = sensor.zone
    created_commands = []

    if sensor.sensor_type != Sensor.SensorType.SOIL_MOISTURE:
        return created_commands

    if not zone.active:
        return created_commands

    rules = IrrigationRule.objects.select_related(
        "actuator",
        "actuator__device",
        "zone",
        "sensor",
    ).filter(
        zone=zone,
        sensor=sensor,
        active=True,
        actuator__active=True,
        actuator__device__active=True,
    )

    now = timezone.now()

    for rule in rules:
        if reading.value > rule.min_threshold:
            continue

        recent_command_exists = Command.objects.filter(
            actuator=rule.actuator,
            rule=rule,
            created_at__gte=now - timedelta(minutes=rule.cooldown_minutes),
            status__in=[
                Command.Status.PENDING,
                Command.Status.SENT,
                Command.Status.EXECUTED,
            ],
        ).exists()

        if recent_command_exists:
            continue

        if rule.actuator.actuator_type in [Actuator.ActuatorType.PUMP, Actuator.ActuatorType.RELAY]:
            command_value = Command.CommandType.TURN_ON
        else:
            command_value = Command.CommandType.OPEN

        command = Command.objects.create(
            zone=rule.zone,
            device=rule.actuator.device,
            actuator=rule.actuator,
            rule=rule,
            command=command_value,
            source=Command.Source.RULE,
            status=Command.Status.PENDING,
            desired_duration_minutes=rule.duration_minutes,
            payload={
                "trigger_sensor_id": rule.sensor.id,
                "trigger_sensor_name": rule.sensor.name,
                "reading_value": str(reading.value),
                "threshold": str(rule.min_threshold),
                "rule_name": rule.name,
            },
        )
        
        # Simulamos la ejecución inmediata para este ejemplo
        command.status = Command.Status.EXECUTED
        command.executed_at = now
        command.save()
        
        # Aplicamos el comando al historial
        apply_command_to_actuator(command)

        recent_unacknowledged_alert = Alert.objects.filter(
            alert_type=Alert.AlertType.LOW_MOISTURE,
            zone=zone,
            sensor=sensor,
            acknowledged=False,
            created_at__gte=now - timedelta(minutes=rule.cooldown_minutes),
        ).exists()

        if not recent_unacknowledged_alert:
            Alert.objects.create(
                zone=zone,
                device=rule.actuator.device,
                sensor=sensor,
                actuator=rule.actuator,
                command=command,
                alert_type=Alert.AlertType.LOW_MOISTURE,
                severity=Alert.Severity.MEDIUM,
                title=f"Humedad baja en {zone.name}",
                message=(
                    f"Se registró humedad {reading.value} por debajo del umbral "
                    f"{rule.min_threshold}. Se generó el comando {command_value}."
                ),
            )

        created_commands.append(command)

    return created_commands
