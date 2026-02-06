from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    tecnico_username = serializers.CharField(source="tecnico.username", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "descripcion",
            "prioridad",
            "estado",
            "tecnico",
            "tecnico_username",
            "fecha_creacion",
            "fecha_asignacion",
            "fecha_resolucion",
        ]
