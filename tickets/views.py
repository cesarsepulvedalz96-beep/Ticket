from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Ticket
from .forms import TicketFormCliente, TicketFormAdmin, TicketFormEmpresa, SignUpForm


# --- Dashboard general (solo Empresa/Admin) ---
@login_required
def index(request):
    if request.user.groups.filter(name="Cliente").exists():
        return redirect("tickets:cliente_dashboard")

    tickets = Ticket.objects.all()
    context = {
        "abiertos": tickets.filter(estado="AB").count(),
        "en_proceso": tickets.filter(estado="EP").count(),
        "resueltos": tickets.filter(estado="RS").count(),
        "cerrados": tickets.filter(estado="CR").count(),
        "descartados": tickets.filter(estado="DS").count(),
    }
    return render(request, "index.html", context)


# --- Tickets Empresa/Admin ---
@login_required
def ticket_list(request):
    if request.user.groups.filter(name="Cliente").exists():
        return redirect("tickets:ticket_list_cliente")

    tickets = Ticket.objects.all()
    return render(
        request,
        "ticket/ticket_list.html",
        {
            "tickets": tickets,
            "is_empresa": request.user.groups.filter(name="Empresa").exists(),
            "is_admin": request.user.is_staff,
        },
    )


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    is_cliente = request.user.groups.filter(name="Cliente").exists()
    is_empresa = request.user.groups.filter(name="Empresa").exists()
    is_admin = request.user.is_staff
    is_creator = (ticket.creador == request.user)

    if is_cliente and not is_creator:
        messages.error(request, "No puedes ver este ticket.")
        return redirect("tickets:ticket_list_cliente")

    return render(
        request,
        "ticket/ticket_detail.html",
        {
            "ticket": ticket,
            "is_cliente": is_cliente,
            "is_empresa": is_empresa,
            "is_admin": is_admin,
            "is_creator": is_creator,
        },
    )


# --- Crear Tickets ---
@login_required
def ticket_create(request):
    if request.user.groups.filter(name="Cliente").exists():
        form_class = TicketFormCliente
        success_url = "tickets:ticket_list_cliente"
    else:
        form_class = TicketFormAdmin
        success_url = "tickets:ticket_list"

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            if request.user.groups.filter(name="Cliente").exists():
                ticket.creador = request.user
            ticket.save()
            messages.success(request, "Ticket creado correctamente.")
            return redirect(success_url)
    else:
        form = form_class()

    return render(request, "ticket/ticket_form.html", {"form": form})


# --- Actualizar Tickets ---
@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user.groups.filter(name="Cliente").exists():
        messages.error(request, "No tienes permisos para editar tickets.")
        return redirect("tickets:ticket_list_cliente")

    if request.user.groups.filter(name="Empresa").exists():
        if request.method == "POST":
            form = TicketFormEmpresa(request.POST, instance=ticket)
            if form.is_valid():
                form.save(user=request.user)
                messages.success(request, "Ticket tomado/actualizado correctamente.")
                return redirect("tickets:ticket_detail", pk=pk)
        else:
            form = TicketFormEmpresa(instance=ticket)
        return render(request, "ticket/ticket_form.html", {"form": form, "is_empresa": True})

    if request.user.is_staff:
        if request.method == "POST":
            form = TicketFormAdmin(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, "Ticket actualizado correctamente.")
                return redirect("tickets:ticket_detail", pk=pk)
        else:
            form = TicketFormAdmin(instance=ticket)
        return render(request, "ticket/ticket_form.html", {"form": form, "is_admin": True})


# --- Eliminar Tickets (solo admin) ---
@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para eliminar tickets.")
        return redirect("tickets:ticket_list")

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket eliminado correctamente.")
        return redirect("tickets:ticket_list")

    return render(request, "ticket/ticket_confirm_delete.html", {"ticket": ticket})


# --- Descartar (solo clientes) ---
@login_required
def ticket_descartar(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user != ticket.creador:
        messages.error(request, "No puedes descartar este ticket.")
        return redirect("tickets:ticket_list_cliente")

    if request.method == "POST":
        ticket.estado = "DS"
        ticket.save()
        messages.success(request, "Ticket descartado correctamente.")
        return redirect("tickets:ticket_list_cliente")

    return render(request, "ticket/ticket_confirm_descartar.html", {"ticket": ticket})


# --- Autenticación ---
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            cliente_group, _ = Group.objects.get_or_create(name="Cliente")
            user.groups.add(cliente_group)
            login(request, user)
            messages.success(request, "Registro exitoso. Bienvenido al portal de cliente.")
            return redirect("tickets:cliente_dashboard")
    else:
        form = SignUpForm()
    return render(request, "user/signup.html", {"form": form})


def elegir_rol(request):
    return render(request, "user/elegir_rol.html")


# --- Login Cliente ---
def login_cliente(request):
    return _custom_login(request, "Cliente", "tickets:cliente_dashboard")


# --- Login Empresa ---
def login_empresa(request):
    return _custom_login(request, "Empresa", "tickets:ticket_list")


# --- Login Admin (nuevo) ---
def login_admin(request):
    return _custom_login(request, "Admin", "tickets:index", template="admin/login.html")


# --- Custom Login ---
def _custom_login(request, group_name, success_url, template="user/login.html"):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Admin -> se valida con is_staff
            if group_name == "Admin" and user.is_staff:
                login(request, user)
                return redirect(success_url)

            # Cliente / Empresa -> se valida por grupo
            if user.groups.filter(name=group_name).exists():
                login(request, user)
                return redirect(success_url)

            messages.error(request, f"Tu cuenta no es de {group_name.lower()}.")
    else:
        form = AuthenticationForm()

    return render(request, template, {"form": form, "tipo": group_name})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return render(request, "user/logout.html")


# --- Dashboard Cliente ---
@login_required
def cliente_dashboard(request):
    tickets = Ticket.objects.filter(creador=request.user)
    return render(request, "cliente_dashboard.html", {"tickets": tickets})


# --- Lista de tickets del cliente ---
@login_required
def ticket_list_cliente(request):
    tickets = Ticket.objects.filter(creador=request.user)
    return render(request, "ticket/ticket_list_cliente.html", {"tickets": tickets})
