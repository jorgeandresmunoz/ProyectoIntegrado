from django.shortcuts import render
from .models import Calificacion, Usuario

def main_view(request):
    calificaciones = Calificacion.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'main.html', {
        'calificaciones': calificaciones,
        'usuarios': usuarios
    })
