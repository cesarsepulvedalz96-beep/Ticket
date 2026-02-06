from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion", "prioridad", "estado", "tecnico", "fecha_creacion")
    list_filter = ("estado", "prioridad", "tecnico", "fecha_creacion")
    search_fields = ("descripcion", "tecnico__username")
    ordering = ("-fecha_creacion",)
    date_hierarchy = "fecha_creacion"
