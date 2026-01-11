from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import TareaIndividual
from .models import TareaGrupal

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

        # Si requiere validación, debe elegirse profesor validador
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
        user = kwargs.pop("user", None)  # ✅ CLAVE: aceptar "user" sin romper el ModelForm
        super().__init__(*args, **kwargs)

        # Solo alumnos como colaboradores
        qs = User.objects.filter(role="ALUMNO").order_by("username")

        # Excluir al creador para que no se meta como colaborador
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