from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('desactivar_usuario/<int:id>/', views.desactivar_usuario, name='desactivar_usuario'),
]
