# alumnos/urls.py
from django.urls import path
from . import views
from .views import lista_alumnos, crear_alumno


urlpatterns = [
    path('', views.lista_alumnos, name='lista_alumnos'),

    path('nuevo/', crear_alumno, name='nuevo_alumno'),
    path('editar/<int:alumno_id>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:alumno_id>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('descargar_reporte/', views.descargar_reporte_alumnos, name='descargar_reporte_alumnos'),

    # ... puedes agregar más URLs específicas para esta aplicación ...
]
