# personal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Personal
from .forms import PersonalForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rango_superior_required
from django.db.models import Q
from nucleos.models import Nucleo
import json, csv
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError


@login_required
def lista_personal(request):
    query = request.GET.get('q', '')  
    nucleo_query = request.GET.get('nucleo', '')
    nucleos = Nucleo.objects.all() 

    if request.user.es_superior():
        personal = Personal.objects.all()
    else:
        personal = Personal.objects.filter(nucleo=request.user.nucleo)
        nucleos = Nucleo.objects.filter(id=request.user.nucleo.id) 

    if query:  
        personal = personal.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) |
            Q(edad__icontains=query) |
            Q(fecha_nacimiento__icontains=query) |
            Q(numero_documento__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(cargo__icontains=query) |
            Q(funcion__icontains=query) |
            Q(nivel_educativo__icontains=query) |
            Q(fecha_ingreso__icontains=query) |
            Q(direccion_habitacion__icontains=query) |
            Q(talla_camisa__icontains=query) |
            Q(talla_zapato__icontains=query) |
            Q(cargo__icontains=query) |
            Q(colateral__icontains=query) |
            Q(estatus__icontains=query) 
            
            
        )
    
    if nucleo_query:
        personal = personal.filter(nucleo__nombre__icontains=nucleo_query)

    context = {'personal': personal, 'nucleos': nucleos} 

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('personal/fragmento_lista_personal.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'personal/lista_personal.html', context)


@login_required
def crear_personal(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                personal = form.save(commit=False)
                personal.full_clean() 
                personal.save()
                return redirect('lista_personal')
            except ValidationError as e:
                errors = e.message_dict if hasattr(e, 'message_dict') else {'__all__': e.messages}
                for field, messages in errors.items():
                    for message in messages:
                        form.add_error(field if field != '__all__' else None, message)
    else:
        form = PersonalForm(user=request.user)
    return render(request, 'personal/crear_personal.html', {'form': form})

@login_required
def editar_personal(request, personal_id):
    personal = get_object_or_404(Personal, pk=personal_id)
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal, user=request.user)
        if form.is_valid():
            try:
                personal = form.save(commit=False)
                personal.full_clean()  
                personal.save()
                return redirect('lista_personal')
            except ValidationError as e:
                errors = e.message_dict if hasattr(e, 'message_dict') else {'__all__': e.messages}
                for field, messages in errors.items():
                    for message in messages:
                        form.add_error(field if field != '__all__' else None, message)
    else:
        form = PersonalForm(instance=personal, user=request.user)
    return render(request, 'personal/editar_personal.html', {'form': form})

@login_required
def eliminar_personal(request, personal_id):
    personal = get_object_or_404(Personal, pk=personal_id)
    if request.method == 'POST':
        personal.delete()
        return redirect('lista_personal')
    return render(request, 'personal/eliminar_personal.html', {'personal': personal})



@login_required
def descargar_reporte_personal(request):
    if request.user.es_superior():
        personal = Personal.objects.all()
    else:
        personal = Personal.objects.filter(nucleo=request.user.nucleo)
        nucleo_query = request.user.nucleo.nombre

    if request.user.es_superior():
        nucleo_query = request.GET.get('nucleo', '')
        if nucleo_query:
            personal = personal.filter(nucleo__nombre__icontains=nucleo_query)

    # Crea la respuesta HTTP para el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_personal_{nucleo_query}.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Nombre', 'Apellido', 'Edad', 'Fecha de Nacimiento', 'Número de Documento', 
        'Descripción', 'Cargo', 'Función', 'Nivel Educativo', 'Fecha Ingreso', 
        'Dirección Habitación', 'Talla Camisa', 'Talla Pantalón', 'Talla Zapato', 
        'Colateral', 'Estatus', 'Núcleo'
    ])

    for persona in personal:
        writer.writerow([
            persona.nombre, persona.apellido, persona.edad, persona.fecha_nacimiento, persona.numero_documento,
            persona.descripcion, persona.cargo, persona.funcion, persona.nivel_educativo, persona.fecha_ingreso,
            persona.direccion_habitacion, persona.talla_camisa, persona.talla_pantalon, persona.talla_zapato,
            persona.colateral, persona.get_estatus_display(), persona.nucleo.nombre
        ])

    return response
