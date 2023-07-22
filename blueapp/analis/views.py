from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import SitioWeb, Publicacion

from .utils.publications import ultimas_publicaciones

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
    return HttpResponse("Parámetro enviado y función ejecutada")


def borrar_sitio_web(request, sitio_web_id):
    try:
        sitio_web = SitioWeb.objects.get(pk=sitio_web_id)
        sitio_web.delete()
        return JsonResponse({'mensaje': 'Sitio web eliminado correctamente.'})
    except SitioWeb.DoesNotExist:
        return JsonResponse({'error': 'Sitio web no encontrado.'}, status=404)
