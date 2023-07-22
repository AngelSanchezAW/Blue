from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('get-post/', views.getPost, name='get-post'),
    path('borrar_sitio_web/<int:sitio_web_id>/', views.borrar_sitio_web, name='borrar_sitio_web'),
]
