from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='inizializza_offerta'),
    path('offerte', views.offerte, name='offerte'),
    path('offerte/<slug:slug>', views.offerta_view, name='offerta'),
    # path('salva_modifiche/', views.salva_modifiche, name='salva_modifiche'),
    # path('<slug:slug>', views.pulsanti, name='pulsante'),
    # path('generate_pdf/<int:student_id>/', views.GeneratePDFView.as_view(), name='generate_pdf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
