from django.urls import path
from . import views

app_name = "tareas"

urlpatterns = [
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("mis-tareas/", views.mis_tareas, name="mis_tareas"),
    path("tareas/nueva/individual/", views.crear_tarea_individual, name="crear_tarea_individual"),
    path("tareas/nueva/grupal/", views.crear_tarea_grupal, name="crear_tarea_grupal"),
    path("profesor/validaciones/", views.tareas_pendientes_validacion, name="tareas_pendientes_validacion"),
    path("profesor/validar/<int:tarea_id>/", views.validar_tarea, name="validar_tarea"),

]
