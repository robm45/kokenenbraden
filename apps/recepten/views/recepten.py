from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models.recept import Recept
from ..forms import ReceptForm
from django.contrib import messages
from django.core.paginator import Paginator

def test(request):
    logger.debug("DEBUG from view")
    logger.info("INFO from view")
    logger.error("ERROR from view")


# ✅ Lijst van recepten (openbaar)
def recept_lijst(request):
    # Als gebruiker een nieuwe keuze maakt, opslaan in sessie
    if "per_page" in request.GET:
        try:
            request.session["per_page"] = int(request.GET["per_page"])
        except ValueError:
            request.session["per_page"] = 10  # fallback

    # Ophalen uit sessie of standaardwaarde
    per_page = request.session.get("per_page", 10)
    sortering = request.GET.get("sortering", "asc")   # standaard A-Z

    recepten = Recept.objects.all()

   # sortering toepassen
    if sortering == "desc":
        recepten = recepten.order_by("-naam")
    else:
        recepten = recepten.order_by("naam")


    paginator = Paginator(recepten, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    context = {
        "page_obj": page_obj,
        "per_page": per_page,
        "sortering": sortering,
    }    

    return render(request, "recepten/recept_lijst.html", context)


# ✅ Detail (openbaar)
def recept_detail(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    return render(request, "recepten/recept_detail.html", {"recept": recept})

# ✅ Verwijderen recept (alleen ingelogd)
@login_required
def recept_delete(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    if request.method == "POST":
        recept.delete()
        messages.success(request, "Recept is verwijderd.")
        return redirect("recepten:recept_lijst")
    return render(request, "recepten/recept_confirm_delete.html", {"object": recept})

# ✅ Bewerken recept (alleen ingelogd)
@login_required
def recept_bewerk(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    if request.method == "POST":
        form = ReceptForm(request.POST, request.FILES, instance=recept)
        if form.is_valid():
            form.save()
            messages.success(request, "Recept is succesvol bijgewerkt.")
            return redirect("recepten:recept_detail", pk=recept.pk)
    else:
        form = ReceptForm(instance=recept)
    return render(request, "recepten/recept_invoer.html", {"form": form})

# ✅ Aanmaken recept (alleen ingelogd)
@login_required
def recept_invoer(request):
    if request.method == "POST":
        form = ReceptForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Recept is succesvol toegevoegd.")
            return redirect("recepten:recept_lijst")
    else:
        form = ReceptForm()
    return render(request, "recepten/recept_invoer.html", {"form": form})
