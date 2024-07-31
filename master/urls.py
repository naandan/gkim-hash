from django.urls import path
from . import views

urlpatterns = [
    path('gallery/<str:masteruser>/images', views.gallery, name='gallery'),
    path('gallery/<str:id>/delete', views.gallery_delete, name='gallery_delete'),
    path('home', views.home, name='home'),
]