from django.urls import path, include   # 👈 faltaba include
from rest_framework.routers import DefaultRouter
from . import views
from .views_api import TicketViewSet

app_name = "tickets"

# Router para API
router = DefaultRouter()
router.register(r"api/tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    # --- Dashboard ---
    path("", views.index, name="index"),  # Dashboard de estadísticas

    # --- Tickets ---
    path("tickets/", views.ticket_list, name="ticket_list"),  # Empresa/Admin: ve todos
    path("mis-tickets/", views.ticket_list_cliente, name="ticket_list_cliente"),  # Cliente: solo los suyos
    path("ticket/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("ticket/nuevo/", views.ticket_create, name="ticket_create"),
    path("ticket/<int:pk>/descartar/", views.ticket_descartar, name="ticket_descartar"),
    path("ticket/<int:pk>/editar/", views.ticket_update, name="ticket_update"),
    path("ticket/<int:pk>/eliminar/", views.ticket_delete, name="ticket_delete"),

    # --- Autenticación ---
    path("login/", views.elegir_rol, name="login"),   # 👈 primero elige
    path("login/cliente/", views.login_cliente, name="login_cliente"),
    path("login/empresa/", views.login_empresa, name="login_empresa"),
    path("login/admin/", views.login_admin, name="login_admin"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

    # --- Dashboard Cliente ---
    path("cliente/", views.cliente_dashboard, name="cliente_dashboard"),

    # --- API ---
    path("", include(router.urls)),   # 👈 ahora sí funciona bien
]
