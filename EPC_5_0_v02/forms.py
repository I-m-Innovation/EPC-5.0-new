from django import forms

from .models import Offerta


class InserisciCliente(forms.Form):
    client_name = forms.CharField(label="Nome cliente", max_length=100, error_messages={
        "required": "Your name must not be empty!",
        "max_length": "Please enter a shorter name!"
    })

    partita_iva = forms.CharField(label="Partita IVA", max_length=100, error_messages={
        "required": "Your name must not be empty!",
        "max_length": "Please enter a shorter name!"
    })
