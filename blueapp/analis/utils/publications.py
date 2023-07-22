from analis.models import SitioWeb, Publicacion
from datetime import datetime
import feedparser

def ultimas_publicaciones(numberPostGet):

    sitios_web = SitioWeb.objects.all()
    fecha_actual = datetime.now()

    for sitio_web in sitios_web:
        feed_url = sitio_web.feed_url
        # Descargar y analizar el feed
        feed_url = feedparser.parse(feed_url)
        # Obtener los últimos n posts
        posts = feed_url.entries[:numberPostGet]

        for post in posts:
            titulo = post.title
            url = post.link

            # Verificar si ya existe una Publicacion con la misma URL
            if not Publicacion.objects.filter(url=url).exists():

                # Crear una instancia de Publicacion y asignar los valores
                publicacion = Publicacion(
                    sitio_web=sitio_web,  # Aquí asignamos el objeto sitio_web
                    titulo=titulo,
                    url=url,
                    fecha_creacion = fecha_actual
                )

                # Guardar la publicación en la base de datos
                publicacion.save()

