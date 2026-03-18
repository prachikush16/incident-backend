import random
from datetime import datetime
from django.db import models
from django.conf import settings


def generate_incident_id():
    year = datetime.now().year
    for _ in range(10):
        candidate = f"RMG{random.randint(10000, 99999)}{year}"
        if not Incident.objects.filter(incident_id=candidate).exists():
            return candidate
    raise ValueError("Could not generate a unique incident ID")


class Incident(models.Model):
    PRIORITY_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    STATUS_CHOICES = [('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')]
    REPORTER_TYPE_CHOICES = [('Enterprise', 'Enterprise'), ('Government', 'Government')]

    incident_id = models.CharField(max_length=20, unique=True, editable=False)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incidents')
    reporter_type = models.CharField(max_length=20, choices=REPORTER_TYPE_CHOICES)
    reporter_name = models.CharField(max_length=255)
    reporter_email = models.EmailField()
    reporter_phone = models.CharField(max_length=15)
    details = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')

    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.incident_id = generate_incident_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.incident_id
