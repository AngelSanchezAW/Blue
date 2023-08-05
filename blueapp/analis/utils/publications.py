from analis.models import Publicacion, SitioWeb
from datetime import datetime
import feedparser

def ultimas_publicaciones(todos_sitios, sitios_web_seleccionados, todas_publicaciones, number_post):

    fecha_actual = datetime.now()
    sitios_web_queryset = SitioWeb.objects.all()

    if not todos_sitios:
        sitios_web_queryset = sitios_web_queryset.filter(sitio_web_id__in=sitios_web_seleccionados)

    for sitio_web in sitios_web_queryset:
        feed_url = sitio_web.feed_url
        feed = feedparser.parse(feed_url)

        if todas_publicaciones:
            posts = feed.entries  # Obtener todas las publicaciones disponibles
        else:
            posts = feed.entries[:number_post]  # Obtener un número específico de publicaciones

        for post in posts:
            titulo = post.title
            url = post.link

            if not Publicacion.objects.filter(url=url).exists():
                publicacion = Publicacion(
                    sitio_web=sitio_web,
                    titulo=titulo,
                    url=url,
                    fecha_creacion=fecha_actual
                )
                publicacion.save()