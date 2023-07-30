from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from .models import SitioWeb, Publicacion

from .utils.publications import ultimas_publicaciones

from django.contrib.auth.decorators import user_passes_test

# Vista página de inicio (Index) 
def index(request):
    sitios_web = SitioWeb.objects.all()
    publicaciones = Publicacion.objects.all()
    
    num_publicaciones_por_sitio = {}
    for sitio_web in sitios_web:
        publicaciones_sitio = Publicacion.objects.filter(sitio_web=sitio_web)
        num_publicaciones = publicaciones_sitio.count()
        num_publicaciones_por_sitio[sitio_web] = num_publicaciones

    context = {
        'sitios_web': sitios_web,
        'publicaciones': publicaciones,
        'num_publicaciones_por_sitio': num_publicaciones_por_sitio,
    }
    return render(request, 'analis/index.html', context)

def getPost(request):
    numberPostGet = int(request.GET.get('numberPostGet'))
    ultimas_publicaciones(numberPostGet)
    return redirect('index')

# Vista para borrar, solo accesible para administradores
@user_passes_test(lambda u: u.is_superuser)
def borrar_sitio_web(request, sitio_web_id):
    try:
        sitio_web = SitioWeb.objects.get(pk=sitio_web_id)
        sitio_web.delete()
        return JsonResponse({'mensaje': 'Sitio web eliminado correctamente.'})
    except SitioWeb.DoesNotExist:
        return JsonResponse({'error': 'Sitio web no encontrado.'}, status=404)

# Vista para agregar, solo accesible para administradores
@user_passes_test(lambda u: u.is_superuser)
def agregar_sitio_web(request):
    if request.method == 'POST':
        nombre = request.POST.get('sitioNombre')
        url = request.POST.get('sitioUrl')
        feed_url = request.POST.get('sitioRSS')

        # Guardar el sitio web en la base de datos
        sitio_web = SitioWeb(nombre=nombre, url=url, feed_url=feed_url)
        sitio_web.save()

        return redirect('index')  # Cambiar 'nombre_de_tu_vista' al nombre de la vista donde deseas redirigir después de guardar
    return render(request, 'analis/index.htmll')

# Vista para actualizar, solo accesible para administradores
@user_passes_test(lambda u: u.is_superuser)
def actualizar_sitio_web(request, sitio_web_id):
    sitio_web = get_object_or_404(SitioWeb, pk=sitio_web_id)

    if request.method == 'POST':
        nombre = request.POST.get('actualizarSitioNombre')
        url = request.POST.get('actualizarSitioUrl')
        rss = request.POST.get('actualizarSitioRSS')

        sitio_web.nombre = nombre
        sitio_web.url = url
        sitio_web.feed_url = rss
        sitio_web.save()

        return redirect('index')
    return render(request, 'analis/index.htmll')