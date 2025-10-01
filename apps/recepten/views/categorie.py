from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models.recept import Categorie
from ..forms import CategorieForm
from django.contrib import messages
from ..utils import handle_delete

@login_required
def categorie_lijst(request):
    categories = Categorie.objects.all()
    return render(request, "recepten/categorie_lijst.html", {"categories": categories})

@login_required
def categorie_invoer(request):
    if request.method == "POST":
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categorie toegevoegd.")
            return redirect("recepten:categorie_lijst")
    else:
        form = CategorieForm()
    return render(request, "recepten/categorie_invoer.html", {"form": form})


@login_required
def categorie_delete(request, pk):
    return handle_delete(
        request,
        model=Categorie,
        pk=pk,
        success_url="recepten:categorie_lijst",
        template_name="recepten/categorie_confirm_delete.html",
        object_name="Categorie"
    )
