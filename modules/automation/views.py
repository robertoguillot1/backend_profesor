from rest_framework import viewsets
from .models import IrrigationRule, IrrigationSchedule, SensorReading, Command, Alert
from .serializers import (
    IrrigationRuleSerializer,
    IrrigationScheduleSerializer,
    SensorReadingSerializer,
    CommandSerializer,
    AlertSerializer,
)
from .services import evaluate_reading_and_generate_automation

class IrrigationRuleViewSet(viewsets.ModelViewSet):
    queryset = IrrigationRule.objects.all()
    serializer_class = IrrigationRuleSerializer

class IrrigationScheduleViewSet(viewsets.ModelViewSet):
    queryset = IrrigationSchedule.objects.all()
    serializer_class = IrrigationScheduleSerializer

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    def perform_create(self, serializer):
        reading = serializer.save()
        evaluate_reading_and_generate_automation(reading)

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
