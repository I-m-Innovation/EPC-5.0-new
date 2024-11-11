from django.shortcuts import render, redirect
from django.views import View
from .forms import InserisciCliente
from django.http import HttpResponseRedirect
from slugify import slugify
from .models import Offerta


def pulsanti(request, slug):
    # print(slug)
    offerta = Offerta.objects.get(slug=slug)
    offerta.consumi_cliente = request.POST.get('consumi_annui_cliente')
    data = {}

    return redirect("pulsante")


def offerta_view(request, slug):

    if "salva_modifiche" in request.POST:
        offerta = Offerta.objects.get(slug=slug)
        offerta.consumi_cliente = float(request.POST['consumi_annui_cliente'].replace("kWh", "").replace(".", "").
                                        replace(",", "."))if request.POST['consumi_annui_cliente'] else 0

        offerta.costi_energia_cliente = float(request.POST['costi_energia_cliente'].replace("€", "").replace(".", "").
                                        replace(",", "."))if request.POST['costi_energia_cliente'] else 0
        offerta.save()
    else:
        offerta = Offerta.objects.get(slug=slug)

    print(offerta.consumi_cliente)

    data = {
        'consumi_annui_cliente': f"{round(offerta.consumi_cliente):,} kWh".replace(',', '.') if offerta.consumi_cliente > 0 else ' kWh',
        'costi_energia_cliente': f"{round(offerta.costi_energia_cliente):,2f} €".replace(',', '.') if offerta.costi_energia_cliente else ' $',
    }

    return render(request, "EPC_5_0_v02/offerta.html", context=data)


def inizializza_offerta(request):
    slug = slugify(request.POST['client_name'])
    offerta = Offerta(slug=slugify(slug))
    offerta.save()

    return slug


# Create your views here.
class IndexView(View):
    def get(self, request):
        form = InserisciCliente()

        return render(request, "EPC_5_0_v02/index.html", {
            "form": form
        })

    def post(self, request):
        form = InserisciCliente(request.POST)
        if form.is_valid():
            slug = inizializza_offerta(request)
            return redirect(f"/{slug}")