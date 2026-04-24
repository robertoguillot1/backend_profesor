from django.contrib import admin
from .models import IrrigationRule, IrrigationSchedule, SensorReading, Command, Alert, IrrigationLog

@admin.register(IrrigationLog)
class IrrigationLogAdmin(admin.ModelAdmin):
    list_display = ("zone", "actuator", "start_time", "end_time", "duration_minutes")
    list_filter = ("zone", "actuator")

@admin.register(IrrigationRule)
class IrrigationRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "zone", "sensor", "min_threshold", "active")
    list_filter = ("active",)

@admin.register(IrrigationSchedule)
class IrrigationScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "zone", "days_of_week", "start_time", "active")

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("sensor", "value", "quality", "timestamp")
    list_filter = ("quality",)

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("device", "command", "source", "status", "created_at")
    list_filter = ("status", "source")

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title", "alert_type", "severity", "acknowledged", "created_at")
    list_filter = ("severity", "acknowledged")
