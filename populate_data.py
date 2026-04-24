import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend2.settings')
django.setup()

from modules.farms.models import Farm, Zone
from modules.devices.models import Device, Sensor, Actuator
from modules.automation.models import IrrigationRule, IrrigationSchedule, SensorReading, Command, Alert
from django.utils import timezone

def populate():
    # 1. Farm
    farm = Farm.objects.create(
        name="Granja La Esperanza",
        location="Km 15 Vía Riohacha",
        description="Granja principal de pruebas"
    )
    print(f"Creada granja: {farm}")

    # 2. Zone
    zone = Zone.objects.create(
        farm=farm,
        name="Sector Norte - Tomates",
        code="norte-tomates",
        crop_name="Tomate Chonto",
        area_m2=500,
        irrigation_mode=Zone.IrrigationMode.AUTOMATIC
    )
    print(f"Creada zona: {zone}")

    # 3. Device
    device = Device.objects.create(
        zone=zone,
        device_id="ESP32-001",
        name="Controlador Principal Norte",
        device_type=Device.DeviceType.CONTROLLER,
        status=Device.Status.ONLINE
    )
    print(f"Creado dispositivo: {device}")

    # 4. Sensor
    sensor = Sensor.objects.create(
        device=device,
        zone=zone,
        name="Sensor Humedad Suelo 1",
        sensor_type=Sensor.SensorType.SOIL_MOISTURE,
        unit="%",
        pin="A0"
    )
    print(f"Creado sensor: {sensor}")

    # 5. Actuator
    actuator = Actuator.objects.create(
        device=device,
        zone=zone,
        name="Bomba de Agua Sector 1",
        actuator_type=Actuator.ActuatorType.PUMP,
        pin="D5",
        state=Actuator.State.OFF
    )
    print(f"Creado actuador: {actuator}")

    # 6. Reading
    reading = SensorReading.objects.create(
        sensor=sensor,
        value=25.5,
        quality=SensorReading.Quality.GOOD
    )
    print(f"Creada lectura: {reading}")

    # 7. Rule
    rule = IrrigationRule.objects.create(
        zone=zone,
        sensor=sensor,
        actuator=actuator,
        name="Riego automático por baja humedad",
        min_threshold=30.0,
        duration_minutes=5
    )
    print(f"Creada regla: {rule}")

    # 8. Schedule
    schedule = IrrigationSchedule.objects.create(
        zone=zone,
        actuator=actuator,
        name="Riego matutino diario",
        days_of_week="MON,TUE,WED,THU,FRI,SAT,SUN",
        start_time="06:00:00",
        duration_minutes=10
    )
    print(f"Creada programación: {schedule}")

    print("\n¡Datos de ejemplo creados con éxito!")

if __name__ == "__main__":
    populate()
