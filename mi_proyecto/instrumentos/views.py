# instrumentos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrumento
from .forms import InstrumentoForm
from django.contrib.auth.decorators import login_required
from usuarios.decorators import rango_superior_required 
# instrumentos/views.py
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import csv
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from nucleos.models import Nucleo

@login_required
def lista_instrumentos(request):
    query = request.GET.get('q', '')
    nucleo_query = request.GET.get('nucleo', '')

    instrumentos = Instrumento.objects.all()
    nucleos = Nucleo.objects.all()  # Obtener todos los núcleos para el menú desplegable

    if not request.user.es_superior():
        instrumentos = instrumentos.filter(nucleo=request.user.nucleo)
        nucleos = Nucleo.objects.filter(id=request.user.nucleo.id)  # Solo el núcleo del usuario


    if query:
        instrumentos = instrumentos.filter(
            Q(item__icontains=query) | 
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(medida__icontains=query) |
            Q(color__icontains=query) |
            Q(serial__icontains=query) |
            Q(inventario__icontains=query) |
            Q(accesorio__icontains=query) |
            Q(condicion__icontains=query) |
            Q(ubicacion__icontains=query) |
            Q(procedencia__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(nucleo__nombre__icontains=query) |
            Q(nombre_persona__icontains=query) |
            Q(direccion__icontains=query) |
            Q(numero_expediente_procesal__icontains=query) |
            Q(poliza_seguro__icontains=query) |
            Q(comodato_vigente__icontains=query)
        )
        
    if nucleo_query:
        instrumentos = instrumentos.filter(nucleo__nombre__icontains=nucleo_query)

    # context debe incluir 'nucleos' para el menú desplegable, incluso si está vacío
    context = {'instrumentos': instrumentos, 'nucleos': nucleos}

    return render(request, 'instrumentos/lista_instrumentos.html', context)


@login_required
def crear_instrumento(request):
    if request.method == 'POST':
        form = InstrumentoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_instrumentos')
    else:
        form = InstrumentoForm(user=request.user)
    return render(request, 'instrumentos/crear_instrumento.html', {'form': form})



@login_required
def editar_instrumento(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, pk=instrumento_id)
    if request.method == 'POST':
        form = InstrumentoForm(request.POST, instance=instrumento, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lista_instrumentos')
    else:
        form = InstrumentoForm(instance=instrumento, user=request.user)
    return render(request, 'instrumentos/editar_instrumento.html', {'form': form})

@login_required
def eliminar_instrumento(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, pk=instrumento_id)
    if request.method == 'POST':
        instrumento.delete()
        return redirect('lista_instrumentos')
    return render(request, 'instrumentos/eliminar_instrumento.html', {'instrumento': instrumento})

@login_required
def descargar_reporte_instrumentos(request):
    # Inicia con la consulta base que obtiene todos los instrumentos
    if request.user.es_superior():
        instrumentos = Instrumento.objects.all()
    else:
        instrumentos = Instrumento.objects.filter(nucleo=request.user.nucleo)
        # Establece el núcleo_query al núcleo del usuario, ignorando la selección "Todos los núcleos"
        nucleo_query = request.user.nucleo.nombre

    # Filtra por núcleo si el usuario es superior y el parámetro está presente en la solicitud
    # Elimina el chequeo de "Todos los núcleos" ya que los usuarios básicos no deberían tener esa opción
    if request.user.es_superior():
        nucleo_query = request.GET.get('nucleo', '')
        if nucleo_query:
            instrumentos = instrumentos.filter(nucleo__nombre__icontains=nucleo_query)

    # Crea la respuesta HTTP para el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_instrumentos_{nucleo_query}.csv"'


    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Fecha', 'Póliza de Seguro', 'Nombre Persona', 'Dirección', 
        'Número Expediente Procesal', 'Procedencia', 'Condición', 'Comodato Vigente', 
        'Item', 'Marca', 'Cantidad', 'Modelo', 'Medida', 'Color', 
        'Serial', 'Inventario', 'Accesorio', 'Ubicación', 'Descripción', 'Núcleo'
    ])

    for instrumento in instrumentos:
        writer.writerow([
            instrumento.fecha, instrumento.get_poliza_seguro_display(), instrumento.nombre_persona, instrumento.direccion,
            instrumento.numero_expediente_procesal, instrumento.get_procedencia_display(), instrumento.get_condicion_display(), instrumento.get_comodato_vigente_display(),
            instrumento.item, instrumento.marca, instrumento.cantidad, instrumento.modelo, instrumento.medida, instrumento.color,
            instrumento.serial, instrumento.inventario, instrumento.accesorio, instrumento.ubicacion, instrumento.descripcion, instrumento.nucleo.nombre
        ])

    return response

