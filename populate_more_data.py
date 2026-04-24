import os
import django
import random
from datetime import time, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend2.settings')
django.setup()

from modules.farms.models import Farm, Zone
from modules.devices.models import Device, Sensor, Actuator
from modules.automation.models import IrrigationRule, IrrigationSchedule, SensorReading, Command, Alert, IrrigationLog

def populate_more():
    # 1. Get or Create Farm
    farm, _ = Farm.objects.get_or_create(
        name="Granja La Esperanza",
        defaults={"location": "Km 15 Vía Riohacha", "description": "Granja principal de producción"}
    )

    # 2. Add 4 more Zones (Total 5)
    zone_data = [
        ("Sector Sur - Plátanos", "sur-platanos", "Plátano Hartón", 1200),
        ("Sector Este - Cacao", "este-cacao", "Cacao Fino", 800),
        ("Invernadero A - Flores", "inv-a-flores", "Rosas", 300),
        ("Lote 4 - Maíz", "lote-4-maiz", "Maíz Amarillo", 2000),
    ]

    zones = [Zone.objects.get_or_create(name="Sector Norte - Tomates", farm=farm)[0]] # Existing
    for name, code, crop, area in zone_data:
        z, created = Zone.objects.get_or_create(
            code=code,
            defaults={"farm": farm, "name": name, "crop_name": crop, "area_m2": area}
        )
        zones.append(z)
        if created: print(f"Creada zona: {name}")

    # 3. Add 4 more Devices (Total 5)
    for i in range(2, 6):
        dev_id = f"ESP32-{i:03d}"
        device, created = Device.objects.get_or_create(
            device_id=dev_id,
            defaults={
                "name": f"Nodo de Control {i}",
                "zone": random.choice(zones),
                "device_type": Device.DeviceType.CONTROLLER,
                "status": Device.Status.ONLINE
            }
        )
        if created: print(f"Creado dispositivo: {device.name}")

    # 4. Add more Sensors
    sensor_types = [
        (Sensor.SensorType.SOIL_MOISTURE, "%"),
        (Sensor.SensorType.TEMPERATURE, "°C"),
        (Sensor.SensorType.HUMIDITY, "%"),
        (Sensor.SensorType.RAIN, "mm"),
    ]
    
    all_devices = Device.objects.all()
    for i in range(1, 10):
        device = random.choice(all_devices)
        stype, unit = random.choice(sensor_types)
        sensor, created = Sensor.objects.get_or_create(
            name=f"Sensor {stype.label} {i}",
            device=device,
            defaults={
                "zone": device.zone,
                "sensor_type": stype,
                "unit": unit,
                "pin": f"GPIO{random.randint(1,32)}"
            }
        )
        if created: print(f"Creado sensor: {sensor.name}")

    # 5. Add more Actuators
    act_types = [Actuator.ActuatorType.PUMP, Actuator.ActuatorType.VALVE, Actuator.ActuatorType.RELAY]
    for i in range(1, 7):
        device = random.choice(all_devices)
        atype = random.choice(act_types)
        actuator, created = Actuator.objects.get_or_create(
            name=f"{atype.label} Automática {i}",
            device=device,
            defaults={
                "zone": device.zone,
                "actuator_type": atype,
                "pin": f"RELAY{i}",
                "state": Actuator.State.OFF
            }
        )
        if created: print(f"Creado actuador: {actuator.name}")

    # 6. Add more Rules
    all_sensors = Sensor.objects.filter(sensor_type=Sensor.SensorType.SOIL_MOISTURE)
    all_actuators = Actuator.objects.all()
    for i in range(1, 6):
        sensor = random.choice(all_sensors)
        actuator = random.choice(all_actuators)
        rule, created = IrrigationRule.objects.get_or_create(
            name=f"Regla de protección {i}",
            defaults={
                "zone": sensor.zone,
                "sensor": sensor,
                "actuator": actuator,
                "min_threshold": random.uniform(20.0, 40.0),
                "duration_minutes": random.randint(5, 20)
            }
        )
        if created: print(f"Creada regla: {rule.name}")

    # 7. Add more Schedules
    days = ["MON,WED,FRI", "TUE,THU,SAT", "SUN", "MON,TUE,WED,THU,FRI,SAT,SUN"]
    for i in range(1, 6):
        actuator = random.choice(all_actuators)
        schedule, created = IrrigationSchedule.objects.get_or_create(
            name=f"Horario de riego {i}",
            defaults={
                "zone": actuator.zone,
                "actuator": actuator,
                "days_of_week": random.choice(days),
                "start_time": time(random.randint(5, 10), 0),
                "duration_minutes": random.randint(10, 30)
            }
        )
        if created: print(f"Creada programación: {schedule.name}")

    # 8. Add Historial de Riego (Logs)
    now = timezone.now()
    for i in range(1, 10):
        zone = random.choice(zones)
        actuator = random.choice(all_actuators)
        start = now - timedelta(days=random.randint(1, 7), hours=random.randint(1, 23))
        duration = random.randint(5, 45)
        log = IrrigationLog.objects.create(
            zone=zone,
            actuator=actuator,
            start_time=start,
            end_time=start + timedelta(minutes=duration),
            duration_minutes=duration
        )
        print(f"Creado log de riego para: {zone.name}")

    print("\n¡Base de datos poblada con éxito!")

if __name__ == "__main__":
    populate_more()
