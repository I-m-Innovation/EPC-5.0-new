from django.db import models

# Create your models here.


class Offerta(models.Model):
    date = models.DateTimeField(null=True)
    user = models.CharField(max_length=100, null=True)
    partita_iva = models.CharField(max_length=100, null=True)
    slug = models.SlugField(db_index=True, unique=True)

    # box giallo
    consumi_cliente = models.FloatField(null=True, default=0)
    costi_energia_cliente = models.FloatField(null=True, default=0)
    tariffa_energia_cliente = models.FloatField(null=True)

    nome_cliente = models.CharField(max_length=100)
    costo_fv = models.FloatField(null=True)
    costo_storage = models.FloatField(null=True)
    costo_trainante = models.FloatField(null=True)
    costo_totale = models.FloatField(null=True)
    potenza_installata = models.FloatField(null=True)
    storage_installato = models.FloatField(null=True)
    producibilità_specifica = models.FloatField(null=True)
    produzione_annua = models.FloatField(null=True)

    tipologia_moduli = models.FloatField(null=True)
    crediti_fv = models.FloatField(null=True)
    crediti_storage = models.FloatField(null=True)
    crediti_trainante = models.FloatField(null=True)
    crediti_totale = models.FloatField(null=True)
    risparmio_energetico_trainante = models.FloatField(null=True)
    aliquota = models.FloatField(null=True, default=0.15)

    risparmi_bolletta = models.CharField(max_length=100, null=True)
    risparmio_bolletta_primo_anno = models.FloatField(null=True)
    risparmio_totale_primo_anno = models.FloatField(null=True)
    risparmio_dieci_anni = models.FloatField(null=True)

    importo_leasing = models.FloatField(null=True)
    anticipo_leasing = models.FloatField(null=True)
    prima_rata = models.FloatField(null=True)
    leasing_primo_anno = models.FloatField(null=True)
    delta_leasing_primo_anno = models.FloatField(null=True)
    leasing_secondo_anno = models.FloatField(null=True)
    delta_leasing_secondo_anno = models.FloatField(null=True)
    leasing_terzo_anno = models.FloatField(null=True)
    delta_leasing_terzo_anno = models.FloatField(null=True)
    leasing_quarto_anno = models.FloatField(null=True)
    delta_leasing_quarto_anno = models.FloatField(null=True)
    leasing_quinto_anno = models.FloatField(null=True)
    delta_leasing_quinto_anno = models.FloatField(null=True)
    leasing_sesto_anno = models.FloatField(null=True)
    delta_leasing_sesto_anno = models.FloatField(null=True)
    leasing_settimo_anno = models.FloatField(null=True)
    delta_leasing_settimo_anno = models.FloatField(null=True)
    leasing_ottavo_anno = models.FloatField(null=True)
    delta_leasing_ottavo_anno = models.FloatField(null=True)
    leasing_nono_anno = models.FloatField(null=True)
    delta_leasing_nono_anno = models.FloatField(null=True)
    leasing_decimo_anno = models.FloatField(null=True)
    delta_leasing_decimo_anno = models.FloatField(null=True)

    delta_leasing_totale = models.FloatField(null=True)
    totale_check = models.FloatField(null=True)
    delta_totale_check = models.FloatField(null=True)
    bilancio_primo_anno = models.FloatField(null=True)

    def __str__(self):
        return f'{self.nome_cliente}'
