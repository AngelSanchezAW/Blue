from django.shortcuts import render
from django.http import HttpResponse

from .models import SitioWeb, Publicacion

from .utils.publications import ultimas_publicaciones

def index(request):
    sitios_web = SitioWeb.objects.all()
    publicaciones = Publicacion.objects.all()
    context = {
        'sitios_web': sitios_web,
        'publicaciones': publicaciones
    }
    return render(request, 'analis/index.html', context)

def getPost(request):
    numberPostGet = int(request.GET.get('numberPostGet'))
    ultimas_publicaciones(numberPostGet)
    return HttpResponse("Parámetro enviado y función ejecutada")