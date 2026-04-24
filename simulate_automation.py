import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend2.settings')
django.setup()

from modules.automation.models import SensorReading, Sensor, IrrigationLog, Command, Alert

def simulate_low_moisture():
    sensor = Sensor.objects.get(name="Sensor Humedad Suelo 1")
    print(f"Simulando lectura baja para sensor: {sensor.name}")
    
    # Creamos la lectura (esto disparará la lógica en perform_create si fuera vía API, 
    # pero aquí llamaremos al servicio directamente o simularemos el comportamiento del ViewSet)
    from modules.automation.services import evaluate_reading_and_generate_automation
    
    reading = SensorReading.objects.create(
        sensor=sensor,
        value=15.0, # Por debajo del umbral de 30.0
        quality=SensorReading.Quality.GOOD
    )
    
    print(f"Lectura creada: {reading.value}%")
    
    # Disparamos la automatización
    commands = evaluate_reading_and_generate_automation(reading)
    
    if commands:
        print(f"¡Automatización disparada! Se crearon {len(commands)} comandos.")
        for cmd in commands:
            print(f"Comando: {cmd.command} para {cmd.actuator.name}")
            
        # Verificamos si se creó el log
        logs = IrrigationLog.objects.filter(actuator=commands[0].actuator, end_time__isnull=True)
        if logs.exists():
            print(f"Historial de riego iniciado automáticamente: {logs.first()}")
        
        # Verificamos la alerta
        alerts = Alert.objects.filter(alert_type=Alert.AlertType.LOW_MOISTURE).order_by('-created_at')
        if alerts.exists():
            print(f"Alerta generada: {alerts.first().title}")
    else:
        print("No se generaron comandos. Revisa las reglas.")

if __name__ == "__main__":
    simulate_low_moisture()
