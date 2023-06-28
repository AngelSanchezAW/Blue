from django.db import models

class SitioWeb(models.Model):
    sitio_web_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255)

class Publicacion(models.Model):
    publicacion_id = models.IntegerField(primary_key=True)
    sitio_web = models.ForeignKey(SitioWeb, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    imagen_portada = models.CharField(max_length=255)
    extracto = models.CharField(max_length=250)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Engagement(models.Model):
    engagement_id = models.IntegerField(primary_key=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    reacciones = models.IntegerField()
    comentarios = models.IntegerField()
    veces_compartidas = models.IntegerField()
    comentarios_sitios_web = models.IntegerField()
    total_engagement = models.IntegerField()
