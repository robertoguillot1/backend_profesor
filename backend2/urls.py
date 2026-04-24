from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from modules.farms.views import FarmViewSet, ZoneViewSet
from modules.devices.views import DeviceViewSet, SensorViewSet, ActuatorViewSet
from modules.automation.views import (
    IrrigationRuleViewSet,
    IrrigationScheduleViewSet,
    SensorReadingViewSet,
    CommandViewSet,
    AlertViewSet,
)

router = DefaultRouter()
# Farms
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'zones', ZoneViewSet, basename='zone')
# Hardware
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'actuators', ActuatorViewSet, basename='actuator')
# Automation
router.register(r'rules', IrrigationRuleViewSet, basename='rule')
router.register(r'schedules', IrrigationScheduleViewSet, basename='schedule')
router.register(r'readings', SensorReadingViewSet, basename='reading')
router.register(r'commands', CommandViewSet, basename='command')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # OpenAPI Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI Documentation
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]