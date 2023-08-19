from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('get-post/', views.getPost, name='get-post'),
    path('borrar_sitio_web/<int:sitio_web_id>/', views.borrar_sitio_web, name='borrar_sitio_web'),
    path('agregar_sitio_web/', views.agregar_sitio_web, name='agregar_sitio_web'),
    path('actualizar_sitio_web/<int:sitio_web_id>/', views.actualizar_sitio_web, name='actualizar_sitio_web'),
    path('get_publication_details/', views.get_publication_details, name='get_publication_details'),
]
