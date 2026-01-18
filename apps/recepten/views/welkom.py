from ..models import Categorie
from ..models import GerechtType
from ..models import HoofdIngredienten
from ..models import Recept
from apps.analytics.models import ReceptViewCount
from django.shortcuts import render

def welkom(request):
    """View function for home page site."""

    #Generate counts of some of the main objects
    num_recepten = Recept.objects.all().count()
    num_categories = Categorie.objects.all().count()
    num_hoofdingredienten = HoofdIngredienten.objects.all().count()
    num_gerechttype= GerechtType.objects.all().count()

    # Top 5 meest bezochte recepten
    top_recepten = (
        ReceptViewCount.objects
        .select_related("recept")
        .order_by("-count")[:5]
    )

    laatste_recepten = Recept.objects.order_by("-datum_toegevoegd")[:3]

    context = {
            'num_recepten': num_recepten,
            'num_categories': num_categories,
            'num_hoofdingredienten': num_hoofdingredienten,
            'num_gerechttype': num_gerechttype,
            'top_recepten' : top_recepten,
            'laatste_recepten': laatste_recepten,
    }
    return render(request, "welkom.html", context)
