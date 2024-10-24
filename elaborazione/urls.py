from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('salva_modifiche/', views.home, name='salva_modifiche'),  # URL per salvare le modifiche
] 
