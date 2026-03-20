from rest_framework import serializers
from incident.models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            'id', 'incident_id', 'reporter_type', 'reporter_name',
            'reporter_email', 'reporter_phone', 'details',
            'reported_at', 'priority', 'status'
        ]
        read_only_fields = ['incident_id', 'reported_at', 'reporter_name', 'reporter_email', 'reporter_phone']

    def validate(self, attrs):
        if self.instance and self.instance.status == 'Closed':
            raise serializers.ValidationError("Closed incidents cannot be edited.")
        return attrs
