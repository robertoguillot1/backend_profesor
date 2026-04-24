from rest_framework import serializers
from .models import IrrigationRule, IrrigationSchedule, SensorReading, Command, Alert

class IrrigationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationRule
        fields = "__all__"

class IrrigationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationSchedule
        fields = "__all__"

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = "__all__"

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = "__all__"

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"
