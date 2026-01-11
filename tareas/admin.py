from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Tarea, TareaIndividual, TareaGrupal, TareaEvaluable


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Para editar un usuario existente
    fieldsets = UserAdmin.fieldsets + (
        ("Rol", {"fields": ("role",)}),
    )

    # Para crear un usuario nuevo
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol", {"fields": ("role",)}),
    )

    list_display = ("username", "email", "role", "is_staff")
    list_filter = ("role",)


admin.site.register(Tarea)
admin.site.register(TareaIndividual)
admin.site.register(TareaGrupal)
admin.site.register(TareaEvaluable)
