from django.db import models

# Create your models here.


class Offerta(models.Model):

    slug = models.SlugField(db_index=True, unique=True)

    # box giallo
    consumi_cliente = models.FloatField(null=True, default=0)
    costi_energia_cliente = models.FloatField(null=True, default=float('nan'))
    tariffa_energia_cliente = models.FloatField(null=True)

    nome_cliente = models.CharField(max_length=100)
    costo_fv = models.FloatField(null=True)
    costo_storage = models.FloatField(null=True)
    costo_trainante = models.FloatField(null=True)
    potenza_installata = models.FloatField(null=True)
    storage_installato = models.FloatField(null=True)
    producibilità_specifica = models.FloatField(null=True)
    produzione_annua = models.FloatField(null=True)
    costo_totale = models.FloatField(null=True)

    tipologia_moduli = models.FloatField(null=True)
    crediti_fv = models.FloatField(null=True)
    crediti_storage = models.FloatField(null=True)
    crediti_trainante = models.FloatField(null=True)
    crediti_totale = models.FloatField(null=True)
    risparmio_energetico_trainante = models.FloatField(null=True)
    aliquota = models.FloatField(null=True)
