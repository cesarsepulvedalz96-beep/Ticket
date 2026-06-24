from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    tecnico_username = serializers.CharField(source="tecnico.username", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "asunto",
            "descripcion",
            "area_trabajo",
            "fecha",
            "prioridad",
            "estado",
            "tecnico",
            "tecnico_username",
            "creador",
            "fecha_creacion",
        ]
        read_only_fields = ["creador", "fecha_creacion", "tecnico_username"]
