# instrumentos/urls.py
from django.urls import path
from . import views
from .views import lista_instrumentos, crear_instrumento


urlpatterns = [
    path('', views.lista_instrumentos, name='lista_instrumentos'),
    path('', lista_instrumentos, name='lista_instrumentos'),
    path('nuevo/', crear_instrumento, name='crear_instrumento'),
    path('editar/<int:instrumento_id>/', views.editar_instrumento, name='editar_instrumento'),
    path('eliminar/<int:instrumento_id>/', views.eliminar_instrumento, name='eliminar_instrumento'),
    path('descargar_reporte_instrumentos/', views.descargar_reporte_instrumentos, name='descargar_reporte_instrumentos'),

    # ... puedes agregar más URLs específicas para esta aplicación ...
]