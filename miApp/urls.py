from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from miApp.views import (
    login_view,
    main_view,
    editar_usuario,
    desactivar_usuario,
    desbloquear_usuario,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', main_view, name='main'),
    path('usuarios/<int:id>/editar/', editar_usuario, name='editar_usuario'),
    path('usuarios/<int:id>/desactivar/', desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/<int:id>/desbloquear/', desbloquear_usuario, name='desbloquear_usuario'),
]
