from django.contrib import admin
from incident.models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ['incident_id', 'reporter', 'reporter_type', 'reporter_name', 'priority', 'status', 'reported_at']
    list_filter = ['status', 'priority', 'reporter_type']
    search_fields = ['incident_id', 'reporter__email', 'reporter_name', 'details']
    ordering = ['-reported_at']
    readonly_fields = ['incident_id', 'reported_at']
    fieldsets = (
        ('Incident Info', {
            'fields': ('incident_id', 'reporter', 'reporter_type', 'reported_at')
        }),
        ('Reporter Details', {
            'fields': ('reporter_name', 'reporter_email', 'reporter_phone')
        }),
        ('Incident Details', {
            'fields': ('details', 'priority', 'status')
        }),
    )
