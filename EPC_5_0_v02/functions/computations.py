import pandas as pd


def calcola_risparmio(produzione_annua_val, perdita, tariffa_energia, consumi):
    risparmio = []
    indexes = []
    for i in range(10):
        indexes.append(i + 1)
        if produzione_annua_val != "INSERIRE DATI IMPIANTO":
            # print(produzione_annua_val)
            produzione = float(produzione_annua_val) * pow(1 - perdita, i)
            risparmio.append(min(produzione * tariffa_energia/1000, consumi* tariffa_energia/1000))
            totale_risparmio = sum(risparmio)
        else:
            produzione = "INSERIRE DATI IMPIANTO"
            risparmio.append(produzione)
            totale_risparmio = "INSERIRE DATI IMPIANTO"

    return risparmio


def calcola_aliquota(risparmio_energetico, spesa_totale):
    if risparmio_energetico == 0.05:
        if spesa_totale < 2.5e6:
            aliquota = 0.35
        elif 2.5e6 <= spesa_totale < 10e6:
            aliquota = 0.15
        else:
            aliquota = 0.05
    elif risparmio_energetico == 0.10:
        if spesa_totale < 2.5e6:
            aliquota = 0.40
        elif 2.5e6 <= spesa_totale < 10e6:
            aliquota = 0.10
        else:
            aliquota = 0.05
    else:
        if spesa_totale < 2.5e6:
            aliquota = 0.45
        elif 2.5e6 <= spesa_totale < 10e6:
            aliquota = 0.25
        else:
            aliquota = 0.15

    return aliquota


def calcola_copertura_fv(potenza_installata):
    if potenza_installata < 20:
        tariffa = 1350
    elif 20 <= potenza_installata < 200:
        tariffa = 1060
    elif 200 <= potenza_installata < 600:
        tariffa = 970
    elif 600 <= potenza_installata < 1000:
        tariffa = 860
    else:
        tariffa = 800

    return potenza_installata*tariffa


def calcola_tabella_risparmi(risparmi_bolletta, offerta):
    risparmi_bolletta = [float(i) for i in risparmi_bolletta]

    indexes = [int(number) for number in range(1, 11)]
    # print(risparmi_bolletta)
    altri_risparmi_df = pd.DataFrame(zip(indexes[0:], risparmi_bolletta[0:]), columns=["index", "valore"])
    # print(risparmi_bolletta)
    # print(offerta.crediti_totale)

    offerta.risparmio_dieci_anni = offerta.crediti_totale + sum(risparmi_bolletta) if risparmi_bolletta else 0
    offerta.save()
    # print(type(risparmi_bolletta))
    risparmio_string = []
    for risparmio in altri_risparmi_df.itertuples():
        risparmio_temp = "{0:,.2f}".format(risparmio.valore)
        risparmio_string.append(f'{risparmio_temp} €')
        altri_risparmi_df_string = pd.DataFrame(zip(indexes[1:], risparmio_string[1:]), columns=["index", "valore"])

    return altri_risparmi_df_string
