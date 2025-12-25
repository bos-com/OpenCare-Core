"""
Admin configuration for appointments.
"""

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Read-only admin for viewing appointments.
    """

    list_display = [
        "patient",
        "provider",
        "facility",
        "start_time",
        "end_time",
        "status",
    ]
    list_filter = ["status", "facility", "provider"]
    search_fields = [
        "patient__first_name",
        "patient__last_name",
        "provider__first_name",
        "provider__last_name",
        "facility__name",
    ]
    ordering = ["-start_time"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "notifications_sent",
        "created_by",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
