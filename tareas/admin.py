from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Tarea, TareaIndividual, TareaGrupal, TareaEvaluable

# Register your models here.
admin.site.register(Usuario, UserAdmin)
admin.site.register(Tarea)
admin.site.register(TareaIndividual)
admin.site.register(TareaGrupal)
admin.site.register(TareaEvaluable)