from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import IngredientForm
from django.contrib import messages
from ..utils import handle_delete
from ..models import HoofdIngredienten

@login_required
def ingredient_invoer(request):
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ingrediënt toegevoegd.")
            return redirect("recepten:ingredient_lijst")
    else:
        form = IngredientForm()
    return render(request, "recepten/ingredient_invoer.html", {"form": form})


@login_required
def ingredient_lijst(request):
    ingredienten = HoofdIngredienten.objects.all()
    return render(request, "recepten/ingredient_lijst.html", {"ingredienten": ingredienten})


@login_required
def ingredient_delete(request, pk):
    return handle_delete(
        request,
        model=HoofdIngredienten,
        pk=pk,
        success_url="recepten:ingredient_lijst",
        template_name="recepten/ingredient_confirm_delete.html",
        object_name="Ingrediënt"
    )
