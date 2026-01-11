from django.urls import path
from . import views

app_name = "tareas"

urlpatterns = [
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("mis-tareas/", views.mis_tareas, name="mis_tareas"),
]
