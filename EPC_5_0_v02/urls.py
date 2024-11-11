from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='inizializza_offerta'),
    path('<slug:slug>', views.offerta_view, name='offerta'),
    # path('pulsante', views.pulsanti, name='pulsante'),
]
