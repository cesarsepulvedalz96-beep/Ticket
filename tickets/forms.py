from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket
from django.utils import timezone


# --- Formulario Cliente ---
class TicketFormCliente(forms.ModelForm):
    """El cliente crea el ticket con información básica"""
    class Meta:
        model = Ticket
        fields = ["descripcion", "area_trabajo", "fecha", "asunto"]
        labels = {
            "descripcion": "Descripción del problema",
            "area_trabajo": "Área de trabajo",
            "fecha": "Fecha del incidente",
            "asunto": "Asunto",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "area_trabajo": forms.Select(attrs={"class": "form-select"}),  
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
        }


# --- Formulario Admin ---
class TicketFormAdmin(forms.ModelForm):
    """El administrador puede editar todo el ticket"""
    class Meta:
        model = Ticket
        fields = ["descripcion", "area_trabajo", "fecha", "asunto", "prioridad", "estado", "tecnico"]
        labels = {
            "descripcion": "Descripción",
            "area_trabajo": "Área de trabajo",
            "fecha": "Fecha",
            "asunto": "Asunto",
            "prioridad": "Prioridad",
            "estado": "Estado",
            "tecnico": "Técnico asignado",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "area_trabajo": forms.Select(attrs={"class": "form-select"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "prioridad": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "tecnico": forms.Select(attrs={"class": "form-select"}),
        }


# --- Formulario Empresa ---
class TicketFormEmpresa(forms.ModelForm):
    """La empresa solo puede tomar el ticket y cambiar su estado"""
    class Meta:
        model = Ticket
        fields = ["estado"]  # solo estado visible
        labels = {
            "estado": "Estado del ticket",
        }
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def save(self, commit=True, user=None):
        ticket = super().save(commit=False)
        if user:
            ticket.tecnico = user  # se asigna automáticamente al usuario de la empresa
            ticket.fecha = timezone.now().date()  # se guarda la fecha en que se tomó el ticket
        if commit:
            ticket.save()
        return ticket


# --- Formulario de Registro ---
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Correo electrónico"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
