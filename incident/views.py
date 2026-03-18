from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from incident.models import Incident
from incident.serializers import IncidentSerializer
from users.serializers import UserSerializer


class IncidentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(reporter=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            reporter=user,
            reporter_name=user.get_full_name() or user.username,
            reporter_email=user.email,
            reporter_phone=user.phone,
        )


class IncidentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(reporter=self.request.user)


class IncidentSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incident_id = request.query_params.get('incident_id')
        if not incident_id:
            return Response({'error': 'incident_id query param is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            incident = Incident.objects.get(incident_id=incident_id, reporter=request.user)
            return Response(IncidentSerializer(incident).data)
        except Incident.DoesNotExist:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)


class ReporterAutofillView(APIView):
    """Returns logged-in user's details to pre-fill incident reporter fields."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'reporter_name': user.get_full_name() or user.username,
            'reporter_email': user.email,
            'reporter_phone': user.phone,
        })
