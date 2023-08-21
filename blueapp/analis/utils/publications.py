from analis.models import Publicacion, SitioWeb, Engagement
from django.utils import timezone
import feedparser, requests
from consts import TOKEN, APIKEY


def ultimas_publicaciones(todos_sitios, sitios_web_seleccionados, todas_publicaciones, number_post):

    fecha_actual = timezone.now()
    sitios_web_queryset = SitioWeb.objects.all()
    nuevas_publicaciones = []  # Crear una lista para almacenar las nuevas publicaciones

    if not todos_sitios:
        sitios_web_queryset = sitios_web_queryset.filter(sitio_web_id__in=sitios_web_seleccionados)

    for sitio_web in sitios_web_queryset:
        feed_url = sitio_web.feed_url
        feed = feedparser.parse(feed_url)

        if todas_publicaciones:
            posts = feed.entries  # Obtener todas las publicaciones disponibles
        else:
            posts = feed.entries[:number_post]  # Obtener un número específico de publicaciones

        # Mostrar el numero de publicaciones a analizar.
        num_entries = len(feed.entries)
        print(f"Estas por procesar: {num_entries} publicaciones de {sitio_web.nombre}")    

        for post in posts:
            
            titulo = post.title
            url = post.link

            if not Publicacion.objects.filter(url=url).exists():

                response = getPost(url)
                if response is not None:
                    imagenportada, content = response
                    summary = content
                    
                    # Si no hay imagen de portada, asignar una por defecto
                    if imagenportada is None:
                        imagenportada = "#"
                    image_url = imagenportada

                    publicacion = Publicacion(
                    sitio_web=sitio_web,
                    titulo=titulo,
                    imagen_portada = image_url,
                    extracto = summary,
                    url=url,
                    fecha_creacion=fecha_actual
                    )
                    publicacion.save()
                    nuevas_publicaciones.append(url)  # Agregar la URL a la lista de nuevas publicaciones
                else:
                    print(f"Hay un problema con la url: {url}")    

    analizar_fb(nuevas_publicaciones)


def analizar_fb(nuevas_publicaciones):

    publicaciones_existentes = Publicacion.objects.filter(url__in=nuevas_publicaciones)
    ids_publicaciones_existentes = publicaciones_existentes.values_list('publicacion_id', flat=True)
    # Combinar las dos listas utilizando zip
    publicaciones_combinadas = zip(ids_publicaciones_existentes, publicaciones_existentes)

    for id_publicacion, publicacion in publicaciones_combinadas:
        
        url = f"https://graph.facebook.com/?id={publicacion.url}&fields=engagement&access_token={TOKEN}"

        response = requests.get(url)
        data = response.json()
        engagement = data['engagement']
        reacciones = engagement['reaction_count']
        comentarios = engagement['comment_count']
        veces_compartidas = engagement['share_count']
        comentarios_sitios_web = engagement['comment_plugin_count']
        total_engagement = reacciones + comentarios + veces_compartidas + comentarios_sitios_web

        # Crear un objeto Engagement con los datos obtenidos
        publicacion = Publicacion.objects.get(url=publicacion.url)
        engagement = Engagement(
            publicacion=publicacion,
            reacciones=reacciones,
            comentarios=comentarios,
            veces_compartidas=veces_compartidas,
            comentarios_sitios_web=comentarios_sitios_web,
            total_engagement=total_engagement
        )
        # Guardar el objeto Engagement en la base de datos
        engagement.save()


def getPost(ulrPost):

    url = "https://getpost.azulweb.net/parse"
    headers = {
        "x-api-key": APIKEY
    }
    data = {
        "url": ulrPost
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        parsed_data = response.json()

        imagenportada = parsed_data.get("lead_image_url", "#")
        content = parsed_data.get("content", "#")

        return(imagenportada,content)

    else:
        print("Error:", response.status_code)