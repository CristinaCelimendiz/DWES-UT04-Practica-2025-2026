from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Tarea, TareaGrupal

User = get_user_model()


@login_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by("username")
    return render(request, "tareas/lista_usuarios.html", {"usuarios": usuarios})


@login_required
def mis_tareas(request):
    user = request.user

    # Tareas creadas por mí (cualquier tipo: base + subclases)
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
