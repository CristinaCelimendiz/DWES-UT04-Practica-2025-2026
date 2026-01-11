# Deciosiones tomadas.
He desarrollado una aplicación en Django para la gestión de tareas cumpliendo lo que seindica en el enunciado: gestión de usuarios, creación de tareas de distintos tipos y flujo de validación según el rol.

## Modelado de datos.
  - He extendido el usuario con AbstractUser creando el modelo Usuario con un campo role (ALUMNO/PROFESOR) para distinguir el usuario.
  - He definido un modelo base Tarea con los campos titulo, descripcion, creada_por, fecha_entrega y campos de estado, completa, valida, fechas y usuario que valida.
  - Para distinguir los tres tipos de tareas he usado modelos heredados:
    - **TareaIndividual:** tarea personal sin realciones con otros.
    - **TareaGrupal:** añade realción ManyToMany con Usuario mediante colaboradores para representar la participacion en grupo.
    - **TareaEvaluable:** añade campos nota y feedback.
  - Las relaciones principales usadas son:
    - Foreignkey desde Tarea a Usuario para creador y el profesor validador.
    - ManyToMany en tareas grupales.

## Reglas.
  - El ciclo de tarea se modela con dos estados:
    - Completada, indica que el alumno ha finalizado la tarea.
    - Valida, indica que la tarea ha sido validada por el profesor o por el alumno en caso de que no necesite al profesor.
  - Segun el enunciado:
    - Si no se necesita la validación del profesor el alumno al marcarla como completada se marca tambien como validada.
    - Si necesita validación el alumno solo la marca como completada y queda pendiente del profesor.
  - La vista de profesor muestra tareas que:
    - Necesitan validación.
    - Estan asignadas a ese profesor.
    - Están completadas por el alumno.
    - Aún no están validadas.

## Formularios y validaciones
  - He creado formularios para:
    - Alta de usuarios (alumnos/profesores).
    - Creación de tarea individual.
    - Creación de tarea grupal.
    - Creación de tarea evaluable.
  - He implementado validaciones básicas como:
    - fecha_entrega.
    - Si se marca "requiere validación" es necesario marcar profesor_validador.
    - En tarea grupal se necesita seleccionar al menos a un colaborador.

## Vistas y navegación.
  - Implemento las vistas solicitadas.
    - Mis datos.
    - Listado de usuarios.
    - Mis tareas.
    - Validaciones pendientes.
    - Para evitar confusiones el enlace de alta de usuario solo se muestra a profesores.

## PostgreSQL
- La aplicación está configurada para usar PostgreSQL e incluyo psycopg2-binary como dependencia. Las migraciones se han usado para crear el esquema y mantenerlo. 

## Interfaz
- Es un frontend sencillo, usando plantillas HTML enfocadas a:
  - Formularios funcionales.
  - Listados claros.
  
    
