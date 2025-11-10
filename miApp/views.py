from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Calificacion, Usuario

@login_required
def main_view(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == "calificacion":
            rut = request.POST.get('rut')
            instrumento = request.POST.get('instrumento')
            tipo = request.POST.get('calificacion')
            fecha = request.POST.get('fecha')
            estado = request.POST.get('estado')
            observacion = request.POST.get('observacion', '')

            if not (rut and instrumento and tipo and fecha and estado):
                messages.error(request, "Todos los campos obligatorios deben completarse.")
                return redirect('main')

            Calificacion.objects.create(
                rut_cliente=rut,
                instrumento=instrumento,
                tipo_calificacion=tipo,
                fecha_calificacion=fecha,
                estado=estado,
                observacion=observacion,
            )
            messages.success(request, "Calificación registrada correctamente.")
            return redirect('main')

        # ---- Registrar usuario ----
        elif form_type == "usuario":
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            rol = request.POST.get('rol', 'analista')

            if not (nombre and correo):
                messages.error(request, "Nombre y correo son obligatorios.")
                return redirect('main')

            if Usuario.objects.filter(correo=correo).exists():
                messages.error(request, "Ya existe un usuario con ese correo.")
                return redirect('main')

            Usuario.objects.create(nombre=nombre, correo=correo, rol=rol)
            messages.success(request, "Usuario creado correctamente.")
            return redirect('main')

    calificaciones = Calificacion.objects.all().order_by('-fecha_calificacion')
    usuarios = Usuario.objects.all().order_by('nombre')

    return render(request, 'main.html', {
        'calificaciones': calificaciones,
        'usuarios': usuarios
    })


@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre', usuario.nombre)
        usuario.correo = request.POST.get('correo', usuario.correo)
        usuario.rol = request.POST.get('rol', usuario.rol)
        usuario.save()
        messages.success(request, "Usuario editado correctamente.")
        return redirect('main')

    return render(request, 'editar_usuario.html', {'usuario': usuario})


@login_required
def desactivar_usuario(request, id):
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para desactivar usuarios.")
        return redirect('main')

    usuario = get_object_or_404(Usuario, id=id)
    usuario.activo = False
    usuario.save()
    messages.success(request, f"Usuario '{usuario.nombre}' desactivado correctamente.")
    return redirect('main')
