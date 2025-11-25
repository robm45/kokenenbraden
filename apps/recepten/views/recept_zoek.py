from django.db.models import Q
from ..forms import ReceptZoekForm
from ..models import Recept
from django.shortcuts import render

def recept_zoek(request):
    query = request.GET.get('q', '')  # algemene zoekterm
    categorie = request.GET.get('categorie', '')
    gerecht_type = request.GET.get('gerecht_type', '')
    bereiding_filter = request.GET.get('bereiding_filter', '')

    resultaten = []  # standaard leeg

    if query or categorie or gerecht_type or bereiding_filter:
        qs = Recept.objects.all()

        if query:
            qs = qs.filter(
                Q(ingredienten__icontains=query) | Q(bereiding__icontains=query)
            )
        
        # --- CATEGORIE FILTER --- 
        if categorie:
            qs = qs.filter(categorie__id=categorie)
        
       
        # --- GERECHTTYPE ILTER ---
        if gerecht_type:
            qs = qs.filter(gerecht_type__id=gerecht_type)

        # --- BEREIDINGSTIJD FILTER ----
        if bereiding_filter == "lt30":
            qs = qs.filter(bereidingstijd__lt=30)


        if bereiding_filter == "30to60":
            qs = qs.filter(bereidingstijd__gte=30, bereidingstijd__lte=60)


        if bereiding_filter == "gt60":
            qs = qs.filter(bereidingstijd__gt=60)

        resultaten = qs.distinct()

    context = {
        'form': ReceptZoekForm(request.GET or None),
        'resultaten': resultaten
    }
    return render(request, 'recepten/recept_zoek.html', context)
