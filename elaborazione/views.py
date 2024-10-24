from django.shortcuts import render, redirect

def home(request):
    if request.method == 'POST':
        # Gestisci i dati inviati dal modulo
        costo_impianto = request.POST.get('costoImpianto')
        potenza_installata = request.POST.get('potenzaInstallata')
        storage = request.POST.get('storage')
        produzione_annuale = request.POST.get('produzioneAnnuale')
        risparmio_energetico = request.POST.get('risparmioEnergetico')
        credito_fiscale = request.POST.get('creditoFiscale')

        # Puoi qui salvare i dati nel database o elaborare come necessario

        return redirect('home')  # Reindirizza alla pagina principale

    return render(request, 'index.html')
