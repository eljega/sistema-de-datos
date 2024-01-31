# nucleos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Nucleo
from .forms import NucleoForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rango_superior_required  # Importa el decorador que acabamos de crear
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import csv


@login_required
def lista_nucleos(request):
    query = request.GET.get('q', '')  # Parámetro de búsqueda

    nucleos = Nucleo.objects.all()

    if query:  # Si hay una consulta de búsqueda, filtra los resultados
        nucleos = nucleos.filter(
            Q(nombre__icontains=query) | 
            Q(codigo__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(estatus_inmueble__icontains=query) |
            Q(infraestructura__icontains=query) |
            Q(nombre_responsable__icontains=query)
            # Añade aquí otros campos por los que quieras filtrar 
        )

    context = {'nucleos': nucleos}

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('nucleos/fragmento_lista_nucleos.html', context, request=request)
        return JsonResponse({'html': html})

    return render(request, 'nucleos/lista_nucleos.html', context)



def crear_nucleo(request):
    if request.method == 'POST':
        form = NucleoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_nucleos')
    else:
        form = NucleoForm()
    return render(request, 'nucleos/crear_nucleo.html', {'form': form})

@rango_superior_required(login_url='login')
def editar_nucleo(request, nucleo_id):
    nucleo = get_object_or_404(Nucleo, pk=nucleo_id)
    if request.method == 'POST':
        form = NucleoForm(request.POST, instance=nucleo)
        if form.is_valid():
            form.save()
            return redirect('lista_nucleos')
    else:
        form = NucleoForm(instance=nucleo)
    return render(request, 'nucleos/editar_nucleo.html', {'form': form})

@rango_superior_required(login_url='login')
def eliminar_nucleo(request, nucleo_id):
    nucleo = get_object_or_404(Nucleo, pk=nucleo_id)
    if request.method == 'POST':
        nucleo.delete()
        return redirect('lista_nucleos')
    return render(request, 'nucleos/eliminar_nucleo.html', {'nucleo': nucleo})

@login_required
def descargar_reporte_nucleos(request):
    nucleos = Nucleo.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_nucleos.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Nombre', 'Código', 'Dirección', 'Teléfono', 'Estatus Inmueble', 'Infraestructura', 'Nombre de el responsable'
    ])

    for nucleo in nucleos:
        writer.writerow([
            nucleo.nombre, nucleo.codigo, nucleo.direccion, nucleo.telefono, 
            nucleo.estatus_inmueble, nucleo.infraestructura, nucleo.nombre_responsable,
        ])

    return response
