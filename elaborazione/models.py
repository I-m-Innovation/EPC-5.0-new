from django.db import models

class Impianto(models.Model):
    costo_impianto = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    storage = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    costo_totale = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    produzione_annua = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    # Altri campi possono essere aggiunti qui

    def __str__(self):
        return f"Impianto con costo {self.costo_impianto} e storage {self.storage}"
