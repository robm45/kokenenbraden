from django.db.models import Q, Case, When, IntegerField
from ..forms import ReceptZoekForm
from ..models import Recept
from django.shortcuts import render

def recept_zoek(request):
    query = request.GET.get('q', '')  # algemene zoekterm
    categorie = request.GET.get('categorie', '')
    gerecht_type = request.GET.get('gerecht_type', '')
    bereiding_filter = request.GET.get('bereiding_filter', '')

    #resultaten = []  # standaard leeg
    resultaten = Recept.objects.none() # standaard leeg

    if query or categorie or gerecht_type or bereiding_filter:
        qs = Recept.objects.all()

        if query:
            woorden = query.split()

            zoekquery = Q()
            score = 0

            for woord in woorden:
               zoekquery &= ( 
                   Q(ingredienten__icontains=woord) | 
                   Q(bereiding__icontains=woord) |
                   Q(naam__icontains=woord) |
                   Q(categorie__naam__icontains=woord)
               )
               
            qs = qs.filter(zoekquery)

            # ranking
            qs = qs.annotate(
                score=Case(
                    When(naam__icontains=query, then=4),
                    When(ingredienten__icontains=query, then=3),
                    When(bereiding__icontains=query, then=2),
                    When(categorie__naam__icontains=query, then=1),
                    default=0,
                    output_files=IntegerField()
                )
            ).order_by("-score", "naam")

        # --- CATEGORIE FILTER ---
        if categorie:
            qs = qs.filter(categorie__id=categorie)


        # --- GERECHTTYPE FILTER ---
        if gerecht_type:
            qs = qs.filter(gerecht_type__id=gerecht_type)

        # --- BEREIDINGSTIJD FILTER ----
        if bereiding_filter == "lt30":
            qs = qs.filter(bereidingstijd__lt=30)
        elif bereiding_filter == "30to60":
            qs = qs.filter(bereidingstijd__gte=30, bereidingstijd__lte=60)
        elif bereiding_filter == "gt60":
            qs = qs.filter(bereidingstijd__gt=60)

        resultaten = qs.distinct().order_by("naam")

    context = {
        'form': ReceptZoekForm(request.GET or None),
        'resultaten': resultaten
    }
    return render(request, 'recepten/recept_zoek.html', context)

