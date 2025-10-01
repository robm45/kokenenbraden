from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models.recept import GerechtType
from ..forms import GerechtTypeForm
from django.contrib import messages
from ..utils import handle_delete

@login_required
def gerecht_type_invoer(request):
    if request.method == "POST":
        form = GerechtTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "GerechtType toegevoegd.")
            return redirect("recepten:gerecht_type_lijst")
    else:
        form = GerechtTypeForm()
    return render(request, "recepten/gerecht_type_invoer.html", {"form": form})


@login_required
def gerecht_type_lijst(request):
    typen = GerechtType.objects.all()
    return render(request, "recepten/gerecht_type_lijst.html", {"typen": typen})


@login_required
def gerecht_type_delete(request, pk):
    return handle_delete(
        request,
        model=GerechtType,
        pk=pk,
        success_url="recepten:gerecht_type_lijst",
        template_name="recepten/gerecht_type_confirm_delete.html",
        object_name="GerechtType"
    )
