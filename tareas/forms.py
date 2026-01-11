from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import TareaIndividual, TareaGrupal, Tarea, TareaEvaluable

from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class TareaIndividualForm(forms.ModelForm):
    class Meta:
        model = TareaIndividual
        fields = ["titulo", "descripcion", "fecha_entrega", "requiere_validacion_profesor", "profesor_validador"]
        widgets = {
            "fecha_entrega": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_fecha_entrega(self):
        fecha = self.cleaned_data.get("fecha_entrega")
        if fecha and fecha <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior al momento actual.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        requiere = cleaned.get("requiere_validacion_profesor")
        profe = cleaned.get("profesor_validador")

        if requiere and not profe:
            self.add_error("profesor_validador", "Debes seleccionar un profesor validador si requiere validación.")
        return cleaned

User = get_user_model()


class TareaGrupalForm(forms.ModelForm):
    class Meta:
        model = TareaGrupal
        fields = [
            "titulo",
            "descripcion",
            "fecha_entrega",
            "colaboradores",
            "requiere_validacion_profesor",
            "profesor_validador",
        ]
        widgets = {
            "fecha_entrega": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None) 
        super().__init__(*args, **kwargs)

        qs = User.objects.filter(role="ALUMNO").order_by("username")

        if user is not None:
            qs = qs.exclude(id=user.id)

        self.fields["colaboradores"].queryset = qs
        self.fields["colaboradores"].required = True

    def clean_fecha_entrega(self):
        fecha = self.cleaned_data.get("fecha_entrega")
        if fecha and fecha <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior al momento actual.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        requiere = cleaned.get("requiere_validacion_profesor")
        profe = cleaned.get("profesor_validador")
        cols = cleaned.get("colaboradores")

        if not cols:
            self.add_error("colaboradores", "Debes seleccionar al menos un colaborador.")

        if requiere and not profe:
            self.add_error(
                "profesor_validador",
                "Selecciona un profesor validador si requiere validación."
            )

        return cleaned
    
class ValidarTareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["comentario_validacion"]
        widgets = {
            "comentario_validacion": forms.Textarea(attrs={"rows": 3}),
        }        

class UsuarioAltaForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "role")

User = get_user_model()

class TareaEvaluableForm(forms.ModelForm):
    class Meta:
        model = TareaEvaluable
        fields = ["titulo", "descripcion", "fecha_entrega", "requiere_validacion_profesor", "profesor_validador"]
        widgets = {
            "fecha_entrega": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profesor_validador"].queryset = User.objects.filter(role="PROFESOR").order_by("username")

    def clean_fecha_entrega(self):
        fecha = self.cleaned_data.get("fecha_entrega")
        if fecha and fecha <= timezone.now():
            raise forms.ValidationError("La fecha de entrega debe ser posterior al momento actual.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        requiere = cleaned.get("requiere_validacion_profesor")
        profe = cleaned.get("profesor_validador")

        if requiere and not profe:
            self.add_error("profesor_validador", "Debes seleccionar un profesor validador si requiere validación.")
        return cleaned