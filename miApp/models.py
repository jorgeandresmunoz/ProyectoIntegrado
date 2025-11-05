from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, default='analista')

    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    rut_cliente = models.CharField(max_length=20)
    instrumento = models.CharField(max_length=100)
    tipo_calificacion = models.CharField(max_length=20)
    fecha_calificacion = models.DateField()
    estado = models.CharField(max_length=20, default='vigente')
    # si quieres enlazar con usuario:
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.rut_cliente} - {self.instrumento}"
