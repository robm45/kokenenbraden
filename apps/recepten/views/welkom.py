from ..models import Categorie
from ..models import GerechtType
from ..models import HoofdIngredienten
from ..models import Recept
from django.shortcuts import render

def welkom(request):
    """View function for home page site."""

    #Generate counts of some of the main objects
    num_recepten = Recept.objects.all().count()
    num_categories = Categorie.objects.all().count()
    num_hoofdingredienten = HoofdIngredienten.objects.all().count()
    num_gerechttype= GerechtType.objects.all().count()

    context = {
            'num_recepten': num_recepten,
            'num_categories': num_categories,
            'num_hoofdingredienten': num_hoofdingredienten,
            'num_gerechttype': num_gerechttype,
    }
    return render(request, "recepten/welkom.html", context)