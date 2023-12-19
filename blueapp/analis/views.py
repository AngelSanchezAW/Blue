from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import SitioWeb, Publicacion, Engagement
from django.db.models import Sum
from .utils.publications import ultimas_publicaciones
from .utils.new_ai_post import new_ai_post
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from .utils.forms import DateFilterForm 
from datetime import timedelta
from django.views.decorators.http import require_POST
from bs4 import BeautifulSoup


# Vista página de inicio (Index) 
def index(request):
    sitios_web = SitioWeb.objects.all()

    publicaciones = Publicacion.objects.annotate(
        fecha_truncada=TruncDate('fecha_creacion')
    ).order_by('-fecha_truncada', '-engagement__total_engagement')

    # Procesar el formulario de filtro de fechas
    date_filter_form = DateFilterForm(request.GET)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data['start_date']
        end_date = date_filter_form.cleaned_data['end_date']
        
        if start_date:
            publicaciones = publicaciones.filter(fecha_creacion__gte=start_date)
        if end_date:
            # Incluir publicaciones hasta el final del día
            end_date_next_day = end_date + timedelta(days=1)
            publicaciones = publicaciones.filter(fecha_creacion__lte=end_date_next_day)

        if start_date and end_date:    
            # Después del filtro, ordena por engagement de forma descendente
            publicaciones = publicaciones.order_by('-engagement__total_engagement')    

    # Obtener las variables de fecha del formulario
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    engagement = Engagement.objects.all()

    paginator = Paginator(publicaciones, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
    # Calcular la diferencia para cada página
    page_range = page_obj.paginator.page_range
    if page_obj.paginator.num_pages > 5:
        if page_obj.number <= 3:
            page_range = range(1, 7)
        elif page_obj.number >= page_obj.paginator.num_pages - 3:
            page_range = range(page_obj.paginator.num_pages - 4, page_obj.paginator.num_pages + 1)
        else:
            page_range = range(page_obj.number - 3, page_obj.number + 3)
        
    offset = (page_obj.number - 1) * paginator.per_page  # Calcular el desplazamiento
    num_publicaciones_por_sitio = {}
    for sitio_web in sitios_web:
        publicaciones_sitio = Publicacion.objects.filter(sitio_web=sitio_web)
        num_publicaciones = publicaciones_sitio.count()
        num_publicaciones_por_sitio[sitio_web] = num_publicaciones

    sitios_con_engagement = SitioWeb.objects.annotate(total_engagement=Sum('publicacion__engagement__total_engagement')) 
    # Ordena la lista de sitios por total de engagement de mayor a menor
    sitios_con_engagement = sorted(sitios_con_engagement, key=lambda sitio: sitio.total_engagement or 0, reverse=True)

    # Reemplaza los valores None por cero en la lista de sitios
    for sitio in sitios_con_engagement:
        if sitio.total_engagement is None:
            sitio.total_engagement = 0

    etiquetas = [sitio.nombre for sitio in sitios_con_engagement]
    totales_engagement = [sitio.total_engagement for sitio in sitios_con_engagement]

    context = {
        'sitios_web': sitios_web,
        'publicaciones': publicaciones,
        'num_publicaciones_por_sitio': num_publicaciones_por_sitio,
        'engagement': engagement,
        'page_obj': page_obj,
        'page_range': page_range,
        'offset': offset,
        'sitios_con_engagement': sitios_con_engagement,
        'etiquetas': etiquetas, 
        'totales_engagement': totales_engagement,
        'date_filter_form': date_filter_form,
        'start_date': start_date,  
        'end_date': end_date,  
    }
    return render(request, 'analis/index.html', context)

# Vista para obtener nuevas publicaciones, solo accesible para administradores
@user_passes_test(lambda u: u.is_superuser)
def getPost(request):
    if request.method == 'POST':
        todos_sitios = request.POST.get('todosSitios') == 'on'
        sitios_web_seleccionados = request.POST.getlist('sitiosWeb')
        sitios_web_seleccionados_int = [int(id_str) for id_str in sitios_web_seleccionados if id_str.isdigit()]
        todas_publicaciones = request.POST.get('todasPublicaciones') == 'on'
        number_post_str = request.POST.get('numberPostGet')
        number_post = int(number_post_str) if number_post_str and number_post_str.isdigit() else None

        ultimas_publicaciones(todos_sitios, sitios_web_seleccionados_int, todas_publicaciones, number_post)
    return redirect('/')

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
    return render(request, 'analis/index.html')

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

def get_publication_details(request):
    if request.method == 'GET':
        publicacion_id = request.GET.get('publicacion_id')
        try:
            
            publicacion = Publicacion.objects.get(publicacion_id=publicacion_id)
            sitioweb = publicacion.sitio_web
            nombre_sitioweb = sitioweb.nombre
            url_sitioweb = sitioweb.url
            engagement = Engagement.objects.get(publicacion=publicacion)
            
            data = {
                'nombreSitioWeb': nombre_sitioweb,
                'urlSitioWeb': url_sitioweb,
                'titulo': publicacion.titulo,
                'postUrl': publicacion.url,
                'extracto': publicacion.extracto,
                'imagenPortada': publicacion.imagen_portada,
                'engagemet': engagement.total_engagement,
            }
            return JsonResponse(data)
        except (Publicacion.DoesNotExist, Engagement.DoesNotExist):
            return JsonResponse({'error': 'Publicación o engagement no encontrados'})
    return JsonResponse({'error': 'Invalid request'})

@require_POST
# Vista para actualizar, solo accesible para administradores
@user_passes_test(lambda u: u.is_superuser)
def generate_ia_post(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        titulo = data.get('titulo', '')
        extracto_html = data.get('extracto', '')
        nombreSitioWeb = data.get('nombreSitioWeb', '')
        urlSitioWeb = data.get('urlSitioWeb', '')
        postUrl = data.get('postUrl', '')

        # Utilizar BeautifulSoup para obtener solo el texto del código HTML
        soup = BeautifulSoup(extracto_html, 'html.parser')
        extracto_texto = soup.get_text()

        print(titulo)
        print(nombreSitioWeb)
        print(urlSitioWeb)
        print(postUrl)

        ai_post_instance = new_ai_post(titulo, extracto_texto)

        print('Articulo generado con IA:', ai_post_instance)

        return JsonResponse({'message': 'Datos recibidos con éxito'})
    except json.JSONDecodeError as e:
        # Manejar errores de decodificación JSON
        return JsonResponse({'error': 'Error en la decodificación JSON'}, status=400)