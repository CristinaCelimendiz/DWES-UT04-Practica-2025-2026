from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ALUMNO = "ALUMNO", "Alumno"
        PROFESOR = "PROFESOR", "Profesor"

    role = models.CharField(max_length=10, choices=Rol.choices, default=Rol.ALUMNO)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Tarea(models.Model):
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)

    creada_por = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="tareas_creadas"
    )
    creada_en = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)

    requiere_validacion_profesor = models.BooleanField(default=False)
    profesor_validador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_a_validar",
    )

    completada = models.BooleanField(default=False)
    completada_en = models.DateTimeField(null=True, blank=True)

    validada = models.BooleanField(default=False)
    validada_en = models.DateTimeField(null=True, blank=True)
    validada_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tareas_validadas",
    )

    class Meta:
        ordering = ["-creada_en"]

    def clean(self):
        # fecha_entrega > creada_en (o > ahora si no hay creada_en aún)
        if self.fecha_entrega:
            ref = self.creada_en or timezone.now()
            if self.fecha_entrega <= ref:
                raise ValidationError({"fecha_entrega": "La fecha de entrega debe ser posterior a la creación."})

        # Si requiere validación, debería haber profesor_validador (lo permitimos vacío pero lo avisamos)
        if self.requiere_validacion_profesor and self.profesor_validador is None:
            # No lo hacemos crítico para no bloquear guardados al inicio,
            # pero si quieres hacerlo estricto, conviértelo en ValidationError.
            pass

        # Si hay profesor_validador, debería ser PROFESOR
        if self.profesor_validador and self.profesor_validador.role != Usuario.Rol.PROFESOR:
            raise ValidationError({"profesor_validador": "El validador debe ser un profesor."})

    def __str__(self):
        return self.titulo


class TareaIndividual(Tarea):
    """Tarea individual: no añade campos extra, pero existe como tipo propio."""


class TareaGrupal(Tarea):
    colaboradores = models.ManyToManyField(
        Usuario, blank=True, related_name="tareas_en_colaboracion"
    )

    def clean(self):
        super().clean()
        # Si quieres exigir mínimo 1 colaborador, lo haremos en el formulario (mejor que aquí).


class TareaEvaluable(Tarea):
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)

    def clean(self):
        super().clean()
        # Normalmente evaluable implica validación del profesor
        # (si quieres forzarlo, también lo hacemos en el formulario)
