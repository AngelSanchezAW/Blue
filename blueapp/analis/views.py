from django.shortcuts import render
from django.http import HttpResponse

from .utils.publications import ultimas_publicaciones

def index(request):
    ultimas_publicaciones()
    return HttpResponse("Hello World!")