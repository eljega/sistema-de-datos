# personal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_personal, name='lista_personal'),
    path('nuevo/', views.crear_personal, name='crear_personal'),
    path('editar/<int:personal_id>/', views.editar_personal, name='editar_personal'),
    path('eliminar/<int:personal_id>/', views.eliminar_personal, name='eliminar_personal'),
    path('descargar_reporte/', views.descargar_reporte_personal, name='descargar_reporte_personal'),
]
