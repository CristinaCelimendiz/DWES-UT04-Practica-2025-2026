from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Tarea, TareaGrupal, Usuario

from django.contrib import messages
from django.shortcuts import redirect

from .forms import TareaIndividualForm

from .forms import TareaGrupalForm

from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import ValidarTareaForm

from .forms import UsuarioAltaForm

User = get_user_model()


@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by("username")
    return render(request, "tareas/lista_usuarios.html", {"usuarios": usuarios})


@login_required
def mis_tareas(request):
    user = request.user

    # Tareas creadas por mí
    tareas_creadas = Tarea.objects.filter(creada_por=user)

    # Tareas grupales donde colaboro
    tareas_colaboro = TareaGrupal.objects.filter(colaboradores=user)

    return render(
        request,
        "tareas/mis_tareas.html",
        {
            "tareas_creadas": tareas_creadas,
            "tareas_colaboro": tareas_colaboro,
        },
    )

@login_required
def crear_tarea_individual(request):
    if request.method == "POST":
        form = TareaIndividualForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.creada_por = request.user
            tarea.save()
            messages.success(request, "Tarea individual creada correctamente.")
            return redirect("tareas:mis_tareas")
    else:
        form = TareaIndividualForm()

    return render(request, "tareas/crear_tarea_individual.html", {"form": form})

@login_required
def crear_tarea_grupal(request):
    if request.method == "POST":
        form = TareaGrupalForm(request.POST, user=request.user)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.creada_por = request.user
            tarea.save()
            form.save_m2m()
            messages.success(request, "Tarea grupal creada correctamente.")
            return redirect("tareas:mis_tareas")
    else:
        form = TareaGrupalForm(user=request.user)

    return render(request, "tareas/crear_tarea_grupal.html", {"form": form})

@login_required
def tareas_pendientes_validacion(request):
    if request.user.role != Usuario.Rol.PROFESOR:
        return redirect("tareas:mis_tareas")

    tareas = Tarea.objects.filter(
        requiere_validacion_profesor=True,
        profesor_validador=request.user,
        validada=False,
    ).order_by("fecha_entrega", "-creada_en")

    return render(request, "tareas/tareas_pendientes_validacion.html", {"tareas": tareas})


@login_required
def validar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    # Solo el profesor asignado puede validar
    if tarea.profesor_validador != request.user:
        return redirect("tareas:tareas_pendientes_validacion")

    if request.method == "POST":
        form = ValidarTareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.validada = True
            tarea.validada_en = timezone.now()
            tarea.validada_por = request.user
            tarea.save()
            return redirect("tareas:tareas_pendientes_validacion")
    else:
        form = ValidarTareaForm(instance=tarea)

    return render(request, "tareas/validar_tarea.html", {"tarea": tarea, "form": form})

@login_required
def mis_datos(request):
    return render(request, "tareas/mis_datos.html", {"u": request.user})

@login_required
def alta_usuario(request):
    
    if request.user.role != Usuario.Rol.PROFESOR:
        return redirect("tareas:mis_tareas")

    if request.method == "POST":
        form = UsuarioAltaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("tareas:lista_usuarios")
    else:
        form = UsuarioAltaForm()

    return render(request, "tareas/alta_usuario.html", {"form": form})