from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='inizializza_offerta'),
    path('offerte', views.offerte_view, name='offerte'),
    path('offerte/<slug:slug>', views.offerta_view, name='offerta'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
