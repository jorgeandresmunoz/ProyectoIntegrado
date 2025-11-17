from django.contrib import admin
from .models import Usuario, Calificacion


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "rol", "activo", "bloqueado", "intentos_fallidos")
    search_fields = ("nombre", "correo")
    list_filter = ("rol", "activo", "bloqueado")

    fields = (
        "nombre",
        "correo",
        "rol",
        "activo",
        "password",          
        "intentos_fallidos",
        "bloqueado",
    )

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ("rut_cliente", "instrumento", "tipo_calificacion", "fecha_calificacion", "estado", "creado_por")
    search_fields = ("rut_cliente", "instrumento", "tipo_calificacion")
    list_filter = ("estado", "fecha_calificacion")
