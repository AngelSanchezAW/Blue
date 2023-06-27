from django.contrib import admin

from .models import SitioWeb, Publicacion, Engagement

@admin.register(SitioWeb)
class SitioWebAdmin(admin.ModelAdmin):
    pass

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    pass

@admin.register(Engagement)
class EngagementAdmin(admin.ModelAdmin):
    pass

