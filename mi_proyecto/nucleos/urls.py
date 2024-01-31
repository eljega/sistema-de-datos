# nucleos/urls.py
from django.urls import path
from . import views
from .views import lista_nucleos, crear_nucleo

urlpatterns = [
    path('', views.lista_nucleos, name='lista_nucleos'),
    path('', lista_nucleos, name='lista_nucleo'),
    path('nuevo/', crear_nucleo, name='crear_nucleo'),
    path('editar/<int:nucleo_id>/', views.editar_nucleo, name='editar_nucleo'),
    path('eliminar/<int:nucleo_id>/', views.eliminar_nucleo, name='eliminar_nucleo'),
    path('descargar_reporte/', views.descargar_reporte_nucleos, name='descargar_reporte_nucleos'),

    # Puedes añadir más rutas según necesites
]
