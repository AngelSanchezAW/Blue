from django.shortcuts import render
from django.http import HttpResponse

from .utils.publications import ultimas_publicaciones

def index(request):
    
    return render(request, 'analis/index.html')

def getPost(request):
    numberPostGet = int(request.GET.get('numberPostGet'))
    ultimas_publicaciones(numberPostGet)
    return HttpResponse("Parámetro enviado y función ejecutada")