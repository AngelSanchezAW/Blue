from django.contrib import admin

from .models import SitioWeb, Publicacion, Engagement, ArticuloGenerado

@admin.register(SitioWeb)
class SitioWebAdmin(admin.ModelAdmin):
    pass

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    pass

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    pass

@admin.register(ArticuloGenerado)
class ArticuloGeneradoAdmin(admin.ModelAdmin):
    pass