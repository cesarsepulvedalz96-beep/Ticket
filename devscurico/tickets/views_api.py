from rest_framework import viewsets, permissions
from .models import Ticket
from .serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by("-fecha_creacion")
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo logueados pueden usar la API
