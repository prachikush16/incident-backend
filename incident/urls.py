from django.urls import path
from incident.views import IncidentListCreateView, IncidentDetailView, IncidentSearchView, ReporterAutofillView

urlpatterns = [
    path('', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('search/', IncidentSearchView.as_view(), name='incident-search'),
    path('autofill/', ReporterAutofillView.as_view(), name='reporter-autofill'),
]
