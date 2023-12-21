from analis.models import Publicacion, SitioWeb, Engagement
from django.utils import timezone
import feedparser, requests
from consts import TOKEN, APIKEY


def ultimas_publicaciones(todos_sitios, sitios_web_seleccionados, todas_publicaciones, number_post):

    fecha_actual = timezone.now()
    sitios_web_queryset = SitioWeb.objects.all()
    total_url_analizar = []  # Crear una lista para almacenar las nuevas publicaciones

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

            total_url_analizar.append(url)  
            
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
                else:
                    print(f"Hay un problema con la url: {url}")    
            else:
                print(f"La URL {url} ya existe.")
    analizar_fb(total_url_analizar)


def analizar_fb(total_url_analizar):
    for url in total_url_analizar:
        try:
            # Obtener la Publicacion existente
            publicacion = Publicacion.objects.get(url=url)
        except Publicacion.DoesNotExist:
            print(f"La publicación con URL {url} no existe en la base de datos.")
            continue

        # Construir la URL para la API de Facebook
        url_api = f"https://graph.facebook.com/?id={publicacion.url}&fields=engagement&access_token={TOKEN}"

        print(f"Se ha analizado en Facebook la url {publicacion.url}.")

        # Realizar la solicitud a la API de Facebook
        response = requests.get(url_api)
        try:
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            data = response.json()
            engagement = data['engagement']
            reacciones = engagement['reaction_count']
            comentarios = engagement['comment_count']
            veces_compartidas = engagement['share_count']
            comentarios_sitios_web = engagement['comment_plugin_count']
            total_engagement = reacciones + comentarios + veces_compartidas + comentarios_sitios_web

            print(f"Cuenta con {total_engagement} de engagement.")

            # Intentar obtener el objeto Engagement asociado a la Publicacion
            try:
                engagement_obj = Engagement.objects.get(publicacion=publicacion)
            except Engagement.DoesNotExist:
                # Si no existe, crear uno nuevo con valores predeterminados
                engagement_obj = Engagement(publicacion=publicacion, reacciones=0, comentarios=0, veces_compartidas=0, comentarios_sitios_web=0, total_engagement=0)

            # Actualizar los datos de engagement en el objeto Engagement
            engagement_obj.reacciones = reacciones
            engagement_obj.comentarios = comentarios
            engagement_obj.veces_compartidas = veces_compartidas
            engagement_obj.comentarios_sitios_web = comentarios_sitios_web
            engagement_obj.total_engagement = total_engagement

            # Guardar los cambios en el objeto Engagement
            engagement_obj.save()
            
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a Facebook para la URL {publicacion.url}: {e}")
        except KeyError as e:
            print(f"Error al analizar la respuesta de Facebook para la URL {publicacion.url}: {e}")

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