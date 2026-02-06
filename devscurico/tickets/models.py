from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    AREA_CHOICES = [
        ("IT", "Soporte Técnico"),
        ("HR", "Recursos Humanos"),
        ("FN", "Finanzas"),
        ("MK", "Marketing"),
        ("VN", "Ventas"),
        ("LG", "Legal"),
        ("PR", "Proyectos"),
        ("AD", "Administración"),
        ("OP", "Operaciones"),
        ("AL", "Almacén / Logística"),
        ("QA", "Calidad"),
]

    # Campos del cliente
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()
    area_trabajo = models.CharField(max_length=50, choices=AREA_CHOICES, default="OT")
    fecha = models.DateField(null=True, blank=True)

    # Gestión interna (admin/empresa)
    prioridad = models.CharField(
        max_length=1,
        choices=[("B", "Baja"), ("M", "Media"), ("A", "Alta")],
        default="M"
    )
    estado = models.CharField(
        max_length=2,
        choices=[("AB", "Abierto"), ("EP", "En Proceso"), ("RS", "Resuelto"), ("CR", "Cerrado"), ("DS", "Descartado")],
        default="AB"
    )
    tecnico = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tickets_asignados"
    )

    # Auditoría
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_creados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.asunto}"
