from django import forms
from django.utils import timezone

from .models import TareaIndividual


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
