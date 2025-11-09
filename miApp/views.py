from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Calificacion, Usuario

@login_required
def main_view(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        instrumento = request.POST.get('instrumento')
        tipo = request.POST.get('calificacion')
        fecha = request.POST.get('fecha')
        estado = request.POST.get('estado')
        observacion = request.POST.get('observacion', '')

        if not (rut and instrumento and tipo and fecha and estado):
            messages.error(request, "Todos los campos obligatorios deben completarse.")
            return redirect('main')

        try:
            Calificacion.objects.create(
                rut_cliente=rut,
                instrumento=instrumento,
                tipo_calificacion=tipo,
                fecha_calificacion=fecha,
                estado=estado,
                observacion=observacion,
            )
            messages.success(request, "Calificación registrada correctamente.")
        except Exception:
            messages.error(request, "Ocurrió un problema al guardar la calificación.")
        return redirect('main')

    calificaciones = Calificacion.objects.all().order_by('-fecha_calificacion')
    usuarios = Usuario.objects.all().order_by('nombre')
    return render(request, 'main.html', {'calificaciones': calificaciones, 'usuarios': usuarios})


@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        nuevo_correo = request.POST.get('correo')
        nuevo_rol = request.POST.get('rol')

        usuario.nombre = nuevo_nombre or usuario.nombre
        usuario.correo = nuevo_correo or usuario.correo
        usuario.rol = nuevo_rol or usuario.rol
        usuario.save()

        messages.success(request, "Usuario editado correctamente.")
        return redirect('main')

    return render(request, 'editar_usuario.html', {'usuario': usuario})


@login_required
def desactivar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    try:
        usuario.delete()  # podrías cambiar por usuario.activo=False si agregas ese campo
        messages.success(request, f"Usuario '{usuario.nombre}' eliminado correctamente.")
    except Exception:
        messages.error(request, "No se pudo eliminar el usuario.")
    return redirect('main')
