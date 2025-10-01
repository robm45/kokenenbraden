from django.db import models
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import Lower 
from django.db.models import ProtectedError
from django.core.exceptions import ValidationError


class Categorie(models.Model):
    """Model voor een recept categorie."""
    naam = models.CharField(
        max_length=200,
        unique=True,
        help_text="Vul in een categorie (bijv. Kip, Varkensvlees, Vegetarisch enz)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.naam

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('catalog:categorie-detail', args=[str(self.id)])

    def clean(self):
        super().clean()
        if Categorie.objects.filter(naam__iexact=self.naam).exclude(pk=self.pk).exists():
            raise ValidationError({'naam': "Categorie bestaat al (case insensitive match)"})

    def save(self, *args, **kwargs):
        self.full_clean()  # roept clean() aan, zorgt dat validatie gebeurt voor opslaan
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['naam']

    def gebruik_form(self):
        from recepten.forms import VerwijderCategorieForm
        form = VerwijderCategorieForm(instance=self)
        return form
        

def CategorieBericht(request):
    return render(request, "categorie_bericht.html")

def CategorieLijst(request):                                                                                                                                                                                    
    mijn_categorien = Categorie.objects.all().values()
    template = loader.get_template("catalog/categorie_lijst.html")
    context = {
            "mijn_categorien" : mijn_categorien
            }
    return HttpResponse(template.render(context, request))
 
def InvoerCategorie(request):
    template = loader.get_template("catalog/add_categorie.html")
    return HttpResponse(template.render({},request))
 
def ToevoegenCategorie(request):
    categorienaam = request.POST['categorie']
    nieuwe_categorie = Categorie(naam=categorienaam)
    categorie_exists = Categorie.objects.filter(naam__iexact=nieuwe_categorie)
    if categorie_exists.exists():
        return HttpResponseRedirect(reverse('catalog:categorielijst'))
    else:
        nieuwe_categorie.save()
        return HttpResponseRedirect(reverse('catalog:categorielijst'))

def categorien_verwijderen(request):
    from recepten.forms import VerwijderCategorieForm
    if request.method == 'POST':
        form = VerwijderCategorieForm(request.POST)
        if form.is_valid():
            geselecteerde_categorien = form.cleaned_data['categorien']
            for ct in geselecteerde_categorien:
                try:
                    ct.delete()
                    messages.success(request, f"Categorie '{ct}' is verwijderd.")
                except ProtectedError:
                    messages.error(
                        request,
                        f"Categorie '{ct}' kan niet worden verwijderd omdat het nog gekoppeld is aan één of meer recepten."
                    )
            return redirect('catalog:categorielijst')  # of een andere url
    else:
        form = VerwijderCategorieForm()
    return render(request, 'catalog/categorien_verwijderen.html', {'form': form})

