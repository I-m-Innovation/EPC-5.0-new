from django.shortcuts import render
from .models import Impianto
from decimal import Decimal, InvalidOperation
import pandas as pd

def home(request):
    return render(request, 'index.html')

# Percorsi ai CSV
CSV_PATH = "Cartel3.csv"
ALIQUOTA_CSV_PATH = "aliqutoconcessa.csv"

# Carica il CSV delle aliquote concessa
aliquota_df = pd.read_csv(ALIQUOTA_CSV_PATH)

# Funzione per formattare i valori come valuta in euro
def format_euro(value):
    return f"{value:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

# Funzione per determinare la fascia di copertura
def determine_fascia_copertura(copertura_impianto_euro):
    if copertura_impianto_euro <= Decimal('2500000'):
        return "Valore_2.5M"
    elif copertura_impianto_euro <= Decimal('10000000'):
        return "Valore_10M"
    elif copertura_impianto_euro <= Decimal('50000000'):
        return "Valore_50M"
    else:
        raise ValueError("Copertura impianto superiore a 50.000.000 € non gestita.")

# Funzione per calcolare l'aliquota concessa in percentuale
def calculate_aliquota_concessa_percentuale(potenza_installata, taglia_impianto_coperto, risparmio_energetico_percentuale):
    # Calcola la copertura impianto in euro
    copertura_impianto_euro = potenza_installata * taglia_impianto_coperto
    
    # Determina la fascia di copertura
    try:
        fascia_copertura = determine_fascia_copertura(copertura_impianto_euro)
    except ValueError as e:
        return f"Errore: {e}"
    
    # Seleziona la riga corrispondente al risparmio energetico
    if risparmio_energetico_percentuale == 5:
        aliquota_row = aliquota_df.iloc[0]  # Prima riga per 5%
    elif risparmio_energetico_percentuale == 10:
        aliquota_row = aliquota_df.iloc[1]  # Seconda riga per 10%
    elif risparmio_energetico_percentuale == 15:
        aliquota_row = aliquota_df.iloc[2]  # Terza riga per 15%
    else:
        return "Percentuale di risparmio energetico non valida. Scegli tra 5, 10 o 15."
    
    # Estrai l'aliquota concessa in percentuale dalla fascia di copertura
    try:
        aliquota_percentuale_str = aliquota_row[fascia_copertura]
        aliquota_percentuale = Decimal(aliquota_percentuale_str.replace('%', '').replace(',', '.')) / 100
    except (InvalidOperation, KeyError) as e:
        return f"Errore nella conversione dell'aliquota percentuale: {e}"
    
    return aliquota_percentuale

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
    aliquota_concessa = '0%'
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
    Bolletta_val = Decimal('0')
    
    
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
        risparmio_energetico_percentuale = int(request.POST.get('risparmio_energetico', '0'))
        # Nota: Ho cambiato 'aliquota_concessa' in 'risparmio_energetico' per chiarezza

        try:
            # Conversione dei valori
            costo_impianto_val = Decimal(costo_impianto.replace('€', '').replace('.', '').replace(',', '.')) if costo_impianto else Decimal('0')
            storage_val = Decimal(storage.replace('€', '').replace('.', '').replace(',', '.')) if storage else Decimal('0')
            bene_trainante2_val = Decimal(bene_trainante2.replace('€', '').replace('.', '').replace(',', '.')) if bene_trainante2 else Decimal('0')
            consumi_annui_val = Decimal(consumi_annui.replace('€', '').replace('.', '').replace(',', '.')) if consumi_annui else Decimal('0')
            produzione_annua_val = Decimal(produzione_annua.replace('kWh/kWp', '').replace(',', '.')) if produzione_annua else Decimal('0')
            costi_annui_val = Decimal(costi_annui.replace('€', '').replace('.', '').replace(',', '.')) if costi_annui else Decimal('0')
            potenza_installata_val = Decimal(potenza_installata.replace('kW', '').replace(',', '.')) if potenza_installata else Decimal('0')
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
                impianto_coperto_value = impianto_coperto_row['copertura'].values[0]
                impianto_coperto_val = Decimal(int(impianto_coperto_value))

            else:
                error_message = "Potenza installata non trovata nel CSV"
                impianto_coperto_val = Decimal('0')
    
            if impianto_coperto_val > Decimal('0'):
                # Calcola l'aliquota concessa in percentuale
                aliquota_percentuale = calculate_aliquota_concessa_percentuale(
                    potenza_installata_val,
                    impianto_coperto_val,
                    risparmio_energetico_percentuale
                )
                
                if isinstance(aliquota_percentuale, Decimal):
                    aliquota_concessa_val = aliquota_percentuale
                    aliquota_concessa = f"{aliquota_concessa_val * 100}%"
                else:
                    # In caso di errore durante il calcolo
                    error_message = aliquota_percentuale
                    aliquota_concessa_val = Decimal('0')
            else:
                error_message = "Copertura impianto non valida."
                aliquota_concessa_val = Decimal('0')
    
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
        'aliquota_concessa': aliquota_concessa,
        
        # Dizionari con il decadimento della produzione e il risparmio energetico per ogni anno
        'decadimento_annuale': decadimento_annuale,
        'risparmio_annuo': risparmio_annuo,
        
        'error_message': error_message,
    })
