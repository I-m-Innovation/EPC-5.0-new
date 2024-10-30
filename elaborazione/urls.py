from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('salva_modifiche/', views.calcola_somma, name='salva_modifiche'),
    path('genera_pdf/', views.genera_pdf_pdfkit, name='genera_pdf'),
]
