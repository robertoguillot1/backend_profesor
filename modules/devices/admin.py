from django.contrib import admin
from .models import Device, Sensor, Actuator

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "device_id", "device_type", "status", "active")
    search_fields = ("name", "device_id")
    list_filter = ("device_type", "status", "active")

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "sensor_type", "device", "zone", "active")
    list_filter = ("sensor_type", "active")

@admin.register(Actuator)
class ActuatorAdmin(admin.ModelAdmin):
    list_display = ("name", "actuator_type", "state", "device", "zone", "active")
    list_filter = ("actuator_type", "state", "active")
