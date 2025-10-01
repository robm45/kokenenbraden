from django.db.models import Q
from ..forms import ReceptZoekForm
from ..models import Recept
from django.shortcuts import render

def recept_zoek(request):
    query = request.GET.get('q', '')  # algemene zoekterm
    categorie = request.GET.get('categorie', '')
    gerecht_type = request.GET.get('gerecht_type', '')

    resultaten = []  # standaard leeg

    if query or categorie or gerecht_type:
        qs = Recept.objects.all()

        if query:
            qs = qs.filter(
                Q(ingredienten__icontains=query) | Q(bereiding__icontains=query)
            )
        if categorie:
            qs = qs.filter(categorie__id=categorie)
        if gerecht_type:
            qs = qs.filter(gerecht_type__id=gerecht_type)

        resultaten = qs.distinct()

    context = {
        'form': ReceptZoekForm(request.GET or None),
        'resultaten': resultaten
    }
    return render(request, 'recepten/recept_zoek.html', context)