from django.contrib import admin
from .models import Farm, Zone

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "active", "created_at")
    search_fields = ("name", "location")
    list_filter = ("active",)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "farm", "irrigation_mode", "active")
    search_fields = ("name", "code", "farm__name")
    list_filter = ("irrigation_mode", "active")
