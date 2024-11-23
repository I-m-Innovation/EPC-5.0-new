from datetime import datetime
from .computations import calcola_aliquota, calcola_copertura_fv, calcola_risparmio


def leggi_valore(stringa):
    stringa = stringa.replace("€", "").replace("kWh", "").replace("kW", "").replace("/p", "").replace(" ", "")

    if "," in stringa and "." in stringa:
        valore = float(stringa.replace(".", "").replace(",", ".")) if stringa.replace(".", "").replace(",", ".") != '' \
            else 0
    else:
        valore = float(stringa.replace(",", ".")) if stringa.replace(".", "").replace(",", ".") != '' else 0
    return valore


def salva_modifiche(request, offerta):
    # box giallo
    offerta.consumi_cliente = leggi_valore(request.POST['consumi_annui_cliente']) \
        if request.POST['consumi_annui_cliente'] else 0
    offerta.costi_energia_cliente = leggi_valore(request.POST['costi_energia_cliente']) \
        if request.POST['costi_energia_cliente'] else 0
    offerta.tariffa_energia_cliente = 1000 * offerta.costi_energia_cliente / offerta.consumi_cliente \
        if offerta.consumi_cliente != 0 else 0
    t = datetime.now()
    t2 = t.astimezone()
    # t3 = t2.strftime('%d/%M/%Y %H:%m')
    offerta.date = t2

    # box blu
    offerta.costo_fv = leggi_valore(request.POST['costo_fv']) if request.POST['costo_fv'] else 0
    offerta.costo_storage = leggi_valore(request.POST['costo_storage']) if request.POST['costo_storage'] else 0
    offerta.costo_trainante = leggi_valore(request.POST['costo_trainante']) \
        if request.POST['costo_trainante'] else 0
    offerta.costo_totale = offerta.costo_fv + offerta.costo_storage + offerta.costo_trainante
    offerta.potenza_installata = leggi_valore(request.POST['potenza_installata']) \
        if request.POST['potenza_installata'] else 0
    offerta.storage_installato = leggi_valore(request.POST['storage_installato']) \
        if request.POST['storage_installato'] else 0
    offerta.producibilità_specifica = leggi_valore(request.POST['producibilità_specifica']) \
        if request.POST['producibilità_specifica'] else 0
    offerta.produzione_annua = offerta.producibilità_specifica * offerta.potenza_installata \
        if offerta.producibilità_specifica and offerta.potenza_installata else 0

    # box rosso
    tipologia_moduli = leggi_valore(request.POST['tipologia_moduli'])
    risparmio_energetico_trainante = leggi_valore(request.POST['risparmio_energetico_trainante']) / 100
    aliquota = calcola_aliquota(risparmio_energetico_trainante, offerta.costo_totale)
    copertura_fv = calcola_copertura_fv(offerta.potenza_installata)
    offerta.crediti_fv = tipologia_moduli * aliquota * min(offerta.costo_fv, copertura_fv) if offerta.costo_fv else 0
    offerta.crediti_storage = tipologia_moduli * aliquota * min(offerta.costo_storage, offerta.storage_installato * 900)
    offerta.crediti_trainante = aliquota * offerta.costo_trainante
    offerta.crediti_totale = offerta.crediti_fv + offerta.crediti_storage + offerta.crediti_trainante
    offerta.risparmio_energetico_trainante = risparmio_energetico_trainante
    offerta.tipologia_moduli = tipologia_moduli
    offerta.aliquota = aliquota

    # box verde
    risparmi_bolletta = calcola_risparmio(offerta.produzione_annua, 0.005, offerta.tariffa_energia_cliente)
    offerta.risparmi_bolletta = risparmi_bolletta
    offerta.risparmio_bolletta_primo_anno = risparmi_bolletta[0]
    offerta.risparmio_totale_primo_anno = offerta.risparmio_bolletta_primo_anno + offerta.crediti_totale

    # box grigio
    offerta.importo_leasing = leggi_valore(request.POST['importo_leasing']) if request.POST['importo_leasing'].replace(
        "€", "").replace(".", "").replace(",", ".") else 0
    offerta.anticipo_leasing = leggi_valore(request.POST['anticipo_leasing']) if request.POST[
        'anticipo_leasing'].replace("€", "").replace(".", "").replace(",", ".") else 0
    offerta.prima_rata = leggi_valore(request.POST['prima_rata']) if request.POST['prima_rata'].replace("€",
                                                                                                        "").replace(".",
                                                                                                                    "").replace(
        ",", ".") else 0
    offerta.leasing_primo_anno = offerta.anticipo_leasing + offerta.prima_rata
    offerta.delta_leasing_primo_anno = offerta.risparmio_totale_primo_anno - offerta.leasing_primo_anno
    offerta.leasing_secondo_anno = leggi_valore(request.POST['leasing_secondo_anno'])\
        if request.POST['leasing_secondo_anno'] else 0
    offerta.delta_leasing_secondo_anno = - offerta.leasing_secondo_anno + risparmi_bolletta[1]
    offerta.leasing_terzo_anno = leggi_valore(request.POST['leasing_terzo_anno']) if request.POST[
                                                                                         'leasing_terzo_anno'] else 0
    offerta.delta_leasing_terzo_anno = - offerta.leasing_terzo_anno + risparmi_bolletta[2]
    offerta.leasing_quarto_anno = leggi_valore(request.POST['leasing_quarto_anno']) if request.POST[
                                                                                           'leasing_quarto_anno'] else 0
    offerta.delta_leasing_quarto_anno = - offerta.leasing_quarto_anno + risparmi_bolletta[3]
    offerta.leasing_quinto_anno = leggi_valore(request.POST['leasing_quinto_anno']) \
        if request.POST['leasing_quinto_anno'] else 0
    offerta.delta_leasing_quinto_anno = - offerta.leasing_quinto_anno + risparmi_bolletta[4]
    offerta.leasing_sesto_anno = leggi_valore(request.POST['leasing_sesto_anno']) \
        if request.POST['leasing_sesto_anno'] else 0
    offerta.delta_leasing_sesto_anno = - offerta.leasing_sesto_anno + risparmi_bolletta[5]
    offerta.leasing_settimo_anno = leggi_valore(request.POST['leasing_settimo_anno']) \
        if request.POST['leasing_settimo_anno'] else 0
    offerta.delta_leasing_settimo_anno = - offerta.leasing_settimo_anno + risparmi_bolletta[6]
    offerta.leasing_ottavo_anno = leggi_valore(request.POST['leasing_ottavo_anno']) \
        if request.POST['leasing_ottavo_anno'] else 0
    offerta.delta_leasing_ottavo_anno = - offerta.leasing_ottavo_anno + risparmi_bolletta[7]
    offerta.leasing_nono_anno = leggi_valore(request.POST['leasing_nono_anno']) \
        if request.POST['leasing_nono_anno'] else 0
    offerta.delta_leasing_nono_anno = - offerta.leasing_nono_anno + risparmi_bolletta[8]
    offerta.leasing_decimo_anno = leggi_valore(request.POST['leasing_decimo_anno']) \
        if request.POST['leasing_decimo_anno'] else 0
    offerta.delta_leasing_decimo_anno = - offerta.leasing_decimo_anno + risparmi_bolletta[9]

    offerta.delta_leasing_totale = offerta.risparmio_dieci_anni - offerta.importo_leasing if offerta.risparmio_dieci_anni else 0
    offerta.totale_check = (offerta.leasing_primo_anno + offerta.leasing_secondo_anno + offerta.leasing_terzo_anno +
                            offerta.leasing_quarto_anno + offerta.leasing_quinto_anno + offerta.leasing_sesto_anno +
                            offerta.leasing_settimo_anno + offerta.leasing_ottavo_anno + offerta.leasing_nono_anno
                            + offerta.leasing_decimo_anno)

    offerta.delta_totale_check = offerta.risparmio_dieci_anni - offerta.totale_check \
        if offerta.risparmio_dieci_anni else 0
    offerta.bilancio_dieci_anni = offerta.risparmio_dieci_anni - offerta.importo_leasing \
        if offerta.risparmio_dieci_anni else 0

    offerta.save()

    return risparmi_bolletta
