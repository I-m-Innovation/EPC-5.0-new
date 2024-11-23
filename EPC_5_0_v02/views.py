from django.shortcuts import render, redirect
from django.views import View
from .forms import InserisciCliente
from slugify import slugify
from .models import Offerta
import platform
from django.contrib.auth import authenticate, login, logout
from .functions.value_reader import salva_modifiche
from .functions.computations import calcola_tabella_risparmi
from .functions.value_writer import crea_tabella_leasing
from django.views.decorators.cache import cache_control

os_platform = platform.system()
pdfkit_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf"

if os_platform == "Linux":
    pdfkit_path = "/usr/bin/wkhtmltopdf"
elif os_platform == "Darwin":
    pdfkit_path = "/usr/local/bin/wkhtmltopdf"

url = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login page URL


def login_view(request):
    if request.method == 'POST':
        if request.POST['username']:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('offerte')  # Replace 'home' with the name of your home page URL
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
        else:
            # print("else")
            return redirect('offerte')
    else:
        data = {"url": 'offerte'}

        return render(request, 'registration/login.html', data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def offerta_view(request, slug):
    risparmi_bolletta = None
    offerta = Offerta.objects.get(slug=slug)
    # print(offerta.user)

    if offerta.user == request.user.username:
        if "salva_modifiche" in request.POST:
            risparmi_bolletta = salva_modifiche(request, offerta)

        elif "logout" in request.POST:
            logout(request)

        else:
            offerta = Offerta.objects.get(slug=slug)
            # print(offerta.risparmi_bolletta)

        if risparmi_bolletta:
            altri_risparmi_df_string = calcola_tabella_risparmi(risparmi_bolletta, offerta)

        else:
            altri_risparmi_df_string = []

        leasing_tab = crea_tabella_leasing(offerta)

        data = {
            'slug': offerta.slug,
            'nome_cliente': offerta.nome_cliente,
            'partita_iva': offerta.partita_iva,
            'consumi_annui_cliente': f"{round(offerta.consumi_cliente, 2):,} kWh".replace(',', ';').replace(
                '.', ',').replace(';', '.') if offerta.consumi_cliente > 0 else 'kWh',
            'costi_energia_cliente': f'{"{0:,.2f}".format(offerta.costi_energia_cliente)} €'.replace(
                ',', ';').replace('.', ',').replace(
                ';', '.') if offerta.costi_energia_cliente else '€',
            'tariffa_energia_cliente': f"{round(offerta.tariffa_energia_cliente, 2):,} €/MWh".replace(
                ',', ';').replace('.', ',').replace(
                ';','.') if offerta.costi_energia_cliente else '',
            'costo_fv': f'{"{0:,.2f}".format(offerta.costo_fv)} €'.replace(',', ';').replace(
                ',', ';').replace('.', ',').replace(
                ';', '.') if offerta.costo_fv else '',
            'costo_storage': f'{"{0:,.2f}".format(offerta.costo_storage)} €'.replace(',', ';').replace(
                ',',';').replace('.', ',').replace(
                ';', '.') if offerta.costo_storage else '',
            'costo_trainante': f'{"{0:,.2f}".format(offerta.costo_trainante)} €'.replace(
                ',', ';').replace(',', ';').replace('.', ',').replace(
                ';', '.') if offerta.costo_trainante else '',
            'costo_totale': f'{"{0:,.2f}".format(offerta.costo_totale)} €'.replace(',', ';').replace(
                ',', ';').replace('.', ',').replace(
                ';', '.') if offerta.costo_totale else '',
            'potenza_installata': f"{round(offerta.potenza_installata, 2):,} kW".replace(
                ',' , ';').replace('.', ',').replace(
                ';', '.') if offerta.potenza_installata else '',
            'storage_installato': f"{round(offerta.storage_installato, 2):,} kWh".replace(
                ',' , ';').replace('.', ',').replace(
                ';', '.') if offerta.storage_installato else '',
            'producibilità_specifica': f"{round(offerta.producibilità_specifica, 2):,} kWh/kWp".replace(
                ',', ';').replace('.', ',').replace(
                ';', '.') if offerta.producibilità_specifica else '',
            'produzione_annua': f"{round(offerta.produzione_annua):,} kWh".replace(
                ',', '.') if offerta.produzione_annua else '',
            'crediti_fv': f'{"{0:,.2f}".format(offerta.crediti_fv)} €'.replace(',', ';').replace(
                '.', ',').replace(';' ,'.') if offerta.crediti_fv else '€',
            'crediti_storage': f'{"{0:,.2f}".format(offerta.crediti_storage)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.crediti_storage else '€',
            'crediti_trainante': f'{"{0:,.2f}".format(offerta.crediti_trainante)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.crediti_trainante else '€',
            'crediti_totale': f'{"{0:,.2f}".format(offerta.crediti_totale)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.crediti_totale else '€',
            'risparmio_energetico_trainante': offerta.risparmio_energetico_trainante if offerta.risparmio_energetico_trainante else '%',
            'aliquota': f"{round(100*offerta.aliquota)} %",
            'risparmio_bolletta_primo_anno': f'{"{0:,.2f}".format(offerta.risparmio_bolletta_primo_anno)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.risparmio_bolletta_primo_anno else '€',
            'risparmio_totale_primo_anno': f'{"{0:,.2f}".format(offerta.risparmio_totale_primo_anno)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.risparmio_totale_primo_anno else '€',
            'risparmi_bolletta': altri_risparmi_df_string,
            'risparmio_dieci_anni': f'{"{0:,.2f}".format(offerta.risparmio_dieci_anni)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.risparmio_dieci_anni else '€',
            'importo_leasing': f'{"{0:,.2f}".format(offerta.importo_leasing)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.importo_leasing else '€',
            'anticipo_leasing': f'{"{0:,.2f}".format(offerta.anticipo_leasing)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.importo_leasing else '€',
            'prima_rata': f'{"{0:,.2f}".format(offerta.prima_rata)} €'.replace(',',';').replace('.',',').replace(';','.') if offerta.prima_rata else '€',
            'leasing_primo_anno': f'{"{0:,.2f}".format(offerta.leasing_primo_anno)} €'.replace(".",";").replace(",",".").replace(";",",") if offerta.leasing_primo_anno else '€',
            'delta_leasing_primo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_primo_anno)} €'.replace(".", ";").replace(",",".").replace(";",",") if offerta.leasing_primo_anno else '€',
            'leasing_secondo_anno': f'{"{0:,.2f}".format(offerta.leasing_secondo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                  ",") if offerta.leasing_secondo_anno else '€',
            'delta_leasing_secondo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_secondo_anno)} €'.replace(".", ";").replace(",",
                                                                                                            ".").replace(
                ";", ",") if offerta.delta_leasing_secondo_anno else '€',
            'leasing_terzo_anno': f'{"{0:,.2f}".format(offerta.leasing_terzo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                      ",") if offerta.leasing_terzo_anno else '€',
            'delta_leasing_terzo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_terzo_anno)} €'.replace(".", ";").replace(",",
                                                                                                                ".").replace(
                ";", ",") if offerta.delta_leasing_terzo_anno else '€',
            'leasing_quarto_anno': f'{"{0:,.2f}".format(offerta.leasing_quarto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                  ",") if offerta.leasing_quarto_anno else '€',
            'delta_leasing_quarto_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_quarto_anno)} €'.replace(".", ";").replace(",",
                                                                                                            ".").replace(
                ";", ",") if offerta.delta_leasing_quarto_anno else '€',
            'leasing_quinto_anno': f'{"{0:,.2f}".format(offerta.leasing_quinto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                    ",") if offerta.leasing_quinto_anno else '€',
            'delta_leasing_quinto_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_quinto_anno)} €'.replace(".", ";").replace(",",
                                                                                                              ".").replace(
                ";", ",") if offerta.delta_leasing_quinto_anno else '€',
            'leasing_sesto_anno': f'{"{0:,.2f}".format(offerta.leasing_sesto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                    ",") if offerta.leasing_sesto_anno else '€',
            'delta_leasing_sesto_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_sesto_anno)} €'.replace(".", ";").replace(",",
                                                                                                              ".").replace(
                ";", ",") if offerta.delta_leasing_sesto_anno else '€',
            'leasing_settimo_anno': f'{"{0:,.2f}".format(offerta.leasing_settimo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                  ",") if offerta.leasing_settimo_anno else '€',
            'delta_leasing_settimo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_settimo_anno)} €'.replace(".", ";").replace(",",
                                                                                                            ".").replace(
                ";", ",") if offerta.delta_leasing_settimo_anno else '€',
            'leasing_ottavo_anno': f'{"{0:,.2f}".format(offerta.leasing_ottavo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                      ",") if offerta.leasing_ottavo_anno else '€',
            'delta_leasing_ottavo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_ottavo_anno)} €'.replace(".", ";").replace(",",
                                                                                                                ".").replace(
                ";", ",") if offerta.delta_leasing_ottavo_anno else '€',
            'leasing_nono_anno': f'{"{0:,.2f}".format(offerta.leasing_nono_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                    ",") if offerta.leasing_nono_anno else '€',
            'delta_leasing_nono_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_nono_anno)} €'.replace(".", ";").replace(",", ".").replace(
                ";", ",") if offerta.delta_leasing_nono_anno else '€',
            'leasing_decimo_anno': f'{"{0:,.2f}".format(offerta.leasing_decimo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                                ",") if offerta.leasing_decimo_anno else '€',
            'delta_leasing_decimo_anno': f'{"{0:,.2f}".format(offerta.delta_leasing_decimo_anno)} €'.replace(".", ";").replace(",",
                                                                                                          ".").replace(
                ";", ",") if offerta.delta_leasing_decimo_anno else '€',
            'totale_check': f'{"{0:,.2f}".format(offerta.totale_check)} €'.replace(".", ";").replace(",",
                                                                                                          ".").replace(
                ";", ",") if offerta.delta_totale_check else '€',
            'delta_totale_check': f'{"{0:,.2f}".format(offerta.delta_totale_check)} €'.replace(".", ";").replace(",",
                                                                                              ".").replace(
                ";", ",") if offerta.delta_totale_check else '€',
            'tipologia_pannelli': str(offerta.tipologia_moduli),
            'date': offerta.date.strftime("%d/%m/%Y %H:%M") if offerta.date else "",
            'leasing_tab': leasing_tab,
            'bilancio_dieci_anni': f'{"{0:,.2f}".format(offerta.bilancio_dieci_anni)} €'.replace(".", ";").replace(",",
                                                                                              ".").replace(
                ";", ",") if offerta.bilancio_dieci_anni else ''
        }

        return render(request, "EPC_5_0_v02/offerta.html", context=data)
    else:
        data = {
            "url": slug
        }
        # print(slug)
        return render(request, "registration/login.html", context=data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inizializza_offerta_view(request):
    slug = slugify(request.POST['client_name'])
    offerta = Offerta(slug=slugify(slug))
    offerta.nome_cliente = request.POST['client_name']
    offerta.partita_iva = request.POST['partita_iva']
    offerta.user = request.user
    try:
        offerta.save()
        return slug
    except Exception as err:
        print(err)

        return 'err'


class IndexView(View):
    def get(self, request, client_initial="", p_iva_initial="", message=""):
        form = InserisciCliente()

        form.initial["client_name"] = client_initial
        form.initial["partita_iva"] = p_iva_initial

        return render(request, "EPC_5_0_v02/index.html", {
            "form": form,
            "message": message,
            "url": f"{slugify(client_initial)}"
        })

    def post(self, request):
        form = InserisciCliente(request.POST)
        if form.is_valid():
            slug = inizializza_offerta_view(request)
            client_name = request.POST["client_name"]
            p_iva = request.POST["partita_iva"]
            message = "Cliente già esistente."
            if slug == 'err':
                return IndexView.get(self, request, client_name, p_iva, message)
            else:
                return redirect(f"offerte/{slug}")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def offerte_view(request):
    offerte = Offerta.objects.filter(user=request.user.username).order_by('-date')

    return render(request, "EPC_5_0_v02/offerte.html", {
        "offerte": offerte
    })


