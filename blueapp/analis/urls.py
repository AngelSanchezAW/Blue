from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('get-post/', views.getPost, name='get-post')
]
