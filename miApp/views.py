from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Calificacion, Usuario


def login_view(request):
    """
    Login usando:
    - correo + clave del modelo Usuario
    - bloqueo tras 3 intentos fallidos
    - creación/uso de un User de Django para @login_required
    """
    if request.method == "POST":
        correo = request.POST.get("correo")
        clave = request.POST.get("clave")

        # Buscar Usuario de negocio
        usuario_negocio = Usuario.objects.filter(correo=correo, activo=True).first()

        if not usuario_negocio:
            messages.error(request, "Correo o contraseña incorrectos.")
            return render(request, "registration/login.html")

        # ¿Está bloqueado?
        if usuario_negocio.bloqueado:
            messages.error(
                request,
                "Tu cuenta está BLOQUEADA por intentos fallidos. Contacta al administrador."
            )
            return render(request, "registration/login.html")

        # ¿Tiene contraseña asignada?
        if not usuario_negocio.password:
            messages.error(
                request,
                "Tu usuario no tiene contraseña asignada. Pide al administrador que la configure."
            )
            return render(request, "registration/login.html")

        # Comparar la clave que escribió con la guardada en Usuario
        if clave != usuario_negocio.password:
            usuario_negocio.intentos_fallidos += 1

            if usuario_negocio.intentos_fallidos >= 3:
                usuario_negocio.bloqueado = True
                messages.error(
                    request,
                    "Has alcanzado 3 intentos fallidos. Tu cuenta ha sido BLOQUEADA."
                )
            else:
                restantes = 3 - usuario_negocio.intentos_fallidos
                messages.error(
                    request,
                    f"Correo o contraseña incorrectos. Intentos restantes: {restantes}"
                )

            usuario_negocio.save()
            return render(request, "registration/login.html")

        # === LOGIN CORRECTO ===
        # Resetear intentos
        usuario_negocio.intentos_fallidos = 0
        usuario_negocio.bloqueado = False
        usuario_negocio.save()

        # Crear o actualizar un User de Django para usar @login_required
        user_django, created = User.objects.get_or_create(
            username=correo,
            defaults={"email": correo}
        )

        # Rol admin -> darle permisos de superuser/staff en Django
        if usuario_negocio.rol == "admin":
            user_django.is_superuser = True
            user_django.is_staff = True
        else:
            user_django.is_superuser = False
            # si quieres que sólo admin entre al admin de Django:
            user_django.is_staff = False

        user_django.save()

        # Iniciar sesión en Django
        login(request, user_django)

        return redirect("main")

    # GET -> mostrar formulario
    return render(request, "registration/login.html")

@login_required
def main_view(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        usuario_negocio = None
        if request.user.email:
            usuario_negocio = Usuario.objects.filter(correo=request.user.email).first()

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
                creado_por=usuario_negocio 
            )
            messages.success(request, "Calificación registrada correctamente.")
            return redirect('main')

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

            Usuario.objects.create(
                nombre=nombre,
                correo=correo,
                rol=rol,
                activo=True,
                intentos_fallidos=0,
                bloqueado=False
            )
            messages.success(request, "Usuario creado correctamente.")
            return redirect('main')

    calificaciones = Calificacion.objects.all().order_by('-fecha_calificacion')
    usuarios = Usuario.objects.filter(activo=True).order_by('nombre')

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


@login_required
def desbloquear_usuario(request, id):
    """
    Permite a un superuser DESBLOQUEAR un usuario:
    - pone intentos_fallidos = 0
    - bloqueado = False
    """
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para desbloquear usuarios.")
        return redirect('main')

    usuario = get_object_or_404(Usuario, id=id)
    usuario.intentos_fallidos = 0
    usuario.bloqueado = False
    usuario.save()
    messages.success(request, f"Usuario '{usuario.nombre}' fue desbloqueado correctamente.")
    return redirect('main')
