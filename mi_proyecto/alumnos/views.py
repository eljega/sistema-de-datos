# alumnos/views.py
from django.shortcuts import render, redirect
from .models import Alumno
from nucleos.models import Nucleo
from .forms import AlumnoForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rango_superior_required 
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
import csv


@login_required
def lista_alumnos(request):
    query = request.GET.get('q', '')  # Parámetro de búsqueda
    nucleo_query = request.GET.get('nucleo', '')

    alumnos = Alumno.objects.all()
    nucleos = Nucleo.objects.all()  # Obtener todos los núcleos para el menú desplegable

    if not request.user.es_superior():
        alumnos = alumnos.filter(nucleo=request.user.nucleo)
        nucleos = Nucleo.objects.filter(id=request.user.nucleo.id)  # Solo el núcleo del usuario

    if query:  # Si hay una consulta de búsqueda, filtra los resultados
        alumnos = alumnos.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) |
            Q(edad__icontains=query) |
            Q(fecha_nacimiento__icontains=query) |
            Q(numero_documento__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(tipo_sangre__icontains=query) |
            Q(sexo__icontains=query) |
            Q(nivel_educativo__icontains=query) |
            Q(nombre_de_representante__icontains=query) |
            Q(numero_de_telefono__icontains=query) |
            Q(direccion_de_habitacion__icontains=query) 
            # Añade aquí otros campos por los que quieras filtrar
        )

    if nucleo_query and nucleo_query != "Todos los núcleos":
        alumnos = alumnos.filter(nucleo__nombre__icontains=nucleo_query)

    context = {'alumnos': alumnos, 'nucleos': nucleos}

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('alumnos/fragmento_lista_alumnos.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'alumnos/lista_alumnos.html', context)


@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST, user=request.user)  # Pasamos el usuario al formulario
        if form.is_valid():
            try:
                alumno = form.save(commit=False)
                alumno.full_clean()  # Llama a la validación del modelo
                alumno.save()
                return redirect('lista_alumnos')
            except ValidationError as e:
                # e puede ser una lista o un diccionario, dependiendo de cómo se haya levantado la excepción
                errors = e.message_dict if hasattr(e, 'message_dict') else {'__all__': e.messages}
                for field, messages in errors.items():
                    for message in messages:
                        form.add_error(field if field != '__all__' else None, message)

    else:
        form = AlumnoForm(user=request.user)  # Pasamos el usuario al formulario para un GET request

    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno, user=request.user)  # Pasamos el usuario al formulario
        if form.is_valid():
            try:
                alumno = form.save(commit=False)
                alumno.full_clean()  # Valida el modelo, incluyendo la lógica de edad y fecha de nacimiento
                alumno.save()
                return redirect('lista_alumnos')
            except ValidationError as e:
                errors = e.message_dict if hasattr(e, 'message_dict') else {'__all__': e.messages}
                for field, messages in errors.items():
                    for message in messages:
                        form.add_error(field if field != '__all__' else None, message)
    else:
        form = AlumnoForm(instance=alumno, user=request.user)  # Pasamos el usuario al formulario para un GET request
    
    return render(request, 'alumnos/editar_alumno.html', {'form': form})

@login_required
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def descargar_reporte_alumnos(request):
    # Inicia con la consulta base que obtiene todos los instrumentos
    if request.user.es_superior():
        alumnos = Alumno.objects.all()
    else:
        alumnos = Alumno.objects.filter(nucleo=request.user.nucleo)
        # Establece el núcleo_query al núcleo del usuario, ignorando la selección "Todos los núcleos"
        nucleo_query = request.user.nucleo.nombre

    # Filtra por núcleo si el usuario es superior y el parámetro está presente en la solicitud
    # Elimina el chequeo de "Todos los núcleos" ya que los usuarios básicos no deberían tener esa opción
    if request.user.es_superior():
        nucleo_query = request.GET.get('nucleo', '')
        if nucleo_query:
            alumnos = alumnos.filter(nucleo__nombre__icontains=nucleo_query)

    # Crea la respuesta HTTP para el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_alumnos_{nucleo_query}.csv"'


    # Crear un objeto writer y escribir la cabecera del CSV
    writer = csv.writer(response, delimiter=';')

    writer.writerow(['Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento', 'Núcleo', 'Estatus', 'Tipo de Sangre', 'Sexo', 'Nivel Educativo', 'Nombre de Representante', 'Número de Teléfono', 'Dirección de Habitación'])

    # Escribir los datos filtrados en el archivo CSV
    for alumno in alumnos:
        writer.writerow([
            alumno.nombre, alumno.apellido, alumno.edad, alumno.fecha_nacimiento, alumno.nucleo.nombre, alumno.estatus, alumno.tipo_sangre, alumno.sexo, alumno.nivel_educativo, alumno.nombre_de_representante, alumno.numero_de_telefono, alumno.direccion_de_habitacion
        ])

    return response
