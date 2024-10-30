from django.shortcuts import render
from .models import Impianto
import pdfkit
from decimal import Decimal, InvalidOperation
import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit

def home(request):
    return render(request, 'index.html')

# Percorso al CSV
CSV_PATH = "Cartel3.csv"

# Funzione per formattare i valori come valuta in euro
def format_euro(value):
    return f"{value:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

def calcola_somma(request):
    # Variabili iniziali
    costo_impianto = ''
    storage = ''
    credito_contributo = '0 €'
    bene_trainante2 = ''
    costo_totale_impianto = '0 €'
    credito_fiscale_5_0 = '0 €'
    consumi_annui = ''
    produzione_annua = '0 kWh/kWp'
    tipologia_pannelli = '1.0'
    costi_annui = ''
    potenza_installata = ''
    aliquota_concessa = '0'
    Bolletta_primo_annuo = '0 €'
    risparmio_primo_annuo = '0 €'
    decadimento_annuale = {}
    risparmio_annuo = {}
    error_message = None

    # Inizializzazione valori decimali
    costo_impianto_val = Decimal('0')
    storage_val = Decimal('0')
    credito_contributo_val = Decimal('0')
    bene_trainante2_val = Decimal('0')
    consumi_annui_val = Decimal('0')
    produzione_annua_val = Decimal('0')
    costi_annui_val = Decimal('0')
    potenza_installata_val = Decimal('0')
    aliquota_concessa_val = Decimal('0')
    
    if request.method == 'POST':
        calcolo_solo = request.POST.get('calcolo_solo') == 'True'
        costo_impianto = request.POST.get('costo_impianto', '')
        storage = request.POST.get('storage', '')
        bene_trainante2 = request.POST.get('bene_trainante2', '')
        consumi_annui = request.POST.get('consumiAnnui', '')
        produzione_annua = request.POST.get('produzione_annua', '0')
        tipologia_pannelli = request.POST.get('tipologia_pannelli', '1.0')
        costi_annui = request.POST.get('costiAnnui', '')
        potenza_installata = request.POST.get('potenza_installata', '0')
        aliquota_concessa = request.POST.get('aliquota_concessa', '0%')

        try:
            # Conversione dei valori
            costo_impianto_val = Decimal(costo_impianto.replace('€', '').replace('.', '').replace(',', '.')) if costo_impianto else Decimal('0')
            storage_val = Decimal(storage.replace('€', '').replace('.', '').replace(',', '.')) if storage else Decimal('0')
            bene_trainante2_val = Decimal(bene_trainante2.replace('€', '').replace('.', '').replace(',', '.')) if bene_trainante2 else Decimal('0')
            consumi_annui_val = Decimal(consumi_annui.replace('€', '').replace('.', '').replace(',', '.')) if consumi_annui else Decimal('0')
            produzione_annua_val = Decimal(produzione_annua.replace('kWh/kWp', '').replace(',', '.')) if produzione_annua else Decimal('0')
            costi_annui_val = Decimal(costi_annui.replace('€', '').replace('.', '').replace(',', '.')) if costi_annui else Decimal('0')
            potenza_installata_val = Decimal(potenza_installata.replace('kW', '').replace(',', '.')) if potenza_installata else Decimal('0')
            aliquota_concessa_val = Decimal(aliquota_concessa.replace('%', '').replace(',', '.')) / 100 if aliquota_concessa else Decimal('0')
            tipologia_pannelli_val = Decimal(tipologia_pannelli)

            # Calcolo del costo totale dell'impianto
            somma_val = costo_impianto_val + storage_val
            costo_totale_impianto = format_euro(somma_val)

            # Calcolo "Bolletta primo anno"
            if consumi_annui_val > Decimal('0'):
                Bolletta_val = (consumi_annui_val - produzione_annua_val) * costi_annui_val / consumi_annui_val
                Bolletta_primo_annuo = format_euro(Bolletta_val)
            else:
                Bolletta_primo_annuo = "0 €"

            # Calcolo del credito fiscale 5.0
            credito_fiscale_5_0_val = credito_contributo_val + storage_val + bene_trainante2_val
            credito_fiscale_5_0 = format_euro(credito_fiscale_5_0_val)

            # Calcolo del risparmio primo anno
            risparmio_primo_annuo_val = credito_fiscale_5_0_val + Bolletta_val
            risparmio_primo_annuo = format_euro(risparmio_primo_annuo_val)

            # Lettura del CSV e ricerca di impianto coperto
            df = pd.read_csv(CSV_PATH)
            impianto_coperto_row = df[df['min'] <= float(potenza_installata_val)].iloc[-1:]

            if not impianto_coperto_row.empty:
                impianto_coperto_val = float(impianto_coperto_row['copertura'].values[0])
            else:
                error_message = "Potenza installata non trovata nel CSV"
                impianto_coperto_val = 0.0

            # Calcolo di "A Contributo"
            if impianto_coperto_val and aliquota_concessa_val and tipologia_pannelli_val:
                contributo_calcolato = aliquota_concessa_val * tipologia_pannelli_val*potenza_installata_val * Decimal(impianto_coperto_val)
                credito_contributo_val = min(costo_impianto_val, contributo_calcolato)
                credito_contributo = format_euro(credito_contributo_val)
            else:
                error_message = "Parametri insufficienti per calcolare 'A Contributo'."

            # Calcolo decadimento produzione e risparmio energetico per ogni anno dal 2 al 10
            for anno in range(2, 11):
                # Calcolo della produzione annua con decadimento
                decadimento = produzione_annua_val * (1 - (Decimal('0.005') * (anno - 1)))
                decadimento_annuale[anno] = format_euro(decadimento) + " kWh/kWp"
                
                # Calcolo del risparmio energetico per l'anno corrente
                if consumi_annui_val > Decimal('0'):
                    risparmio_energetico = (consumi_annui_val - decadimento) * costi_annui_val / consumi_annui_val
                    risparmio_annuo[anno] = format_euro(risparmio_energetico)
                else:
                    risparmio_annuo[anno] = "0 €"

            # Salvataggio condizionale
            if not calcolo_solo:
                nuovo_impianto = Impianto.objects.create(
                    costo_impianto=costo_impianto_val,
                    storage=storage_val,
                    produzione_annua=produzione_annua_val,
                )
                nuovo_impianto.save()

        except (InvalidOperation, ValueError, KeyError, IndexError) as e:
            error_message = f"Errore nei dati inseriti o nella lettura del CSV: {e}. Assicurati di inserire valori validi."

    # Passa i valori formattati al template
    return render(request, 'index.html', {
        'costo_impianto': format_euro(costo_impianto_val) if costo_impianto else '',
        'storage': format_euro(storage_val) if storage else '',
        'credito_contributo': credito_contributo,
        'bene_trainante2': format_euro(bene_trainante2_val) if bene_trainante2 else '',
        'costo_totale_impianto': costo_totale_impianto,
        'credito_fiscale_5_0': credito_fiscale_5_0,
        'creditoFiscale': credito_fiscale_5_0,
        'consumi_annui': format_euro(consumi_annui_val) if consumi_annui else '',
        'produzione_annua': produzione_annua,
        'risparmio_primo_annuo': risparmio_primo_annuo,
        'tipologia_pannelli': tipologia_pannelli,
        'costi_annui': format_euro(costi_annui_val) if costi_annui else '',
        'Bolletta_primo_annuo': Bolletta_primo_annuo,
        'potenza_installata': f"{potenza_installata_val} kW",
        'aliquota_concessa': f"{aliquota_concessa_val * 100}%",
        
        # Dizionari con il decadimento della produzione e il risparmio energetico per ogni anno
        'decadimento_annuale': decadimento_annuale,
        'risparmio_annuo': risparmio_annuo,
        
        'error_message': error_message,
    })




def genera_pdf_pdfkit(request):
    # Prepara il contenuto HTML
    html_content = render_to_string('index.html', context={})

    # Configura le opzioni di `pdfkit` per il formato A4 orizzontale
    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'encoding': 'UTF-8',
    }

    # Genera il PDF utilizzando pdfkit
    pdf = pdfkit.from_string(html_content, False, options=options)

    # Ritorna il PDF come risposta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="progetto.pdf"'
    return response