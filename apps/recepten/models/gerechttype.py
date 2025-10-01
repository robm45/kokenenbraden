from django.db import models
from django.db.models.functions import Lower
from django.db.models import ProtectedError
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError

class GerechtType(models.Model):
    """Model voor een recept type (ovenschotel, quiche, tajine etc.)."""
    gerecht_type = models.CharField(
        max_length=200,
        unique=True,
        help_text="Vul in een gerechttype (bijv. Ovenschotel, Quiche  enz)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.gerecht_type

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('recepten:gerecht_type-detail', args=[str(self.id)])

    def clean(self):
        if GerechtType.objects \
            .annotate(gt_lower=Lower('gerecht_type')) \
            .filter(gt_lower=self.gerecht_type.lower()) \
            .exclude(pk=self.pk) \
            .exists():
            raise ValidationError({"gerecht_type": "Gerecht type bestaat al (case insensitive match)."})

    def save(self, *args, **kwargs):
        self.full_clean()  # roept clean() aan, zorgt dat validatie gebeurt voor opslaan
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['gerecht_type']

def GerechtTypeLijst(request):
    mijn_gerechttypen = GerechtType.objects.all().values()
    template = loader.get_template("catalog/gerechttype_lijst.html")
    context = {
            "mijn_gerechttypen" : mijn_gerechttypen
            }
    return HttpResponse(template.render(context, request))

def InvoerGerechtType(request):
    template = loader.get_template("catalog/toevoegen_gerechttype.html")
    return HttpResponse(template.render({},request))

def ToevoegenGerechtType(request):
    gerechttypenaam = request.POST['gerechttype']
    nieuwe_gerechttype = GerechtType(gerecht_type=gerechttypenaam)

    if GerechtType.objects.filter(gerecht_type__iexact=nieuwe_gerechttype).exists():
        return HttpResponseRedirect(reverse('catalog:gerechttypelijst'))
    else:
        nieuwe_gerechttype.save()
        return HttpResponseRedirect(reverse('catalog:gerechttypelijst'))


def gerechttypen_verwijderen(request):
    from recepten.forms import VerwijderGerechtTypeForm
    if request.method == 'POST':
        form = VerwijderGerechtTypeForm(request.POST)
        if form.is_valid():
            geselecteerde_gerechttypen = form.cleaned_data['gerechttypen']
            for gt in geselecteerde_gerechttypen:
                try:
                    gt.delete()
                    messages.success(request, f"Gerechttype '{gt}' is verwijderd.")
                except ProtectedError:
                    messages.error(
                        request,
                        f"Gerechtstype '{gt}' kan niet worden verwijderd omdat het nog gekoppeld is aan één of meer recepten."
                    )
            return redirect('catalog:gerechttypelijst')
    else:
        form = VerwijderGerechtTypeForm()
    return render(request, 'catalog/gerechttypen_verwijderen.html', {'form': form})

