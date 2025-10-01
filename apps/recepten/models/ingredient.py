from django.db import models
from django.db.models.functions import Lower
from django.db.models import ProtectedError
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
#from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError

class HoofdIngredienten(models.Model):
    """Model voor de belangrijkste ingredienten van een recept."""
    ingredient = models.CharField(
        max_length=200,
        unique=True,
        help_text="Kies de belangrijkste ingrediente"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.ingredient

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('catalog:ingredient-detail', args=[str(self.id)])

    def clean(self):
        # Case-insensitive check voor bestaande ingredienten behalve deze zelf
        if HoofdIngredienten.objects.filter(ingredient__iexact=self.ingredient).exclude(pk=self.pk).exists():
            raise ValidationError({'ingredient': "Ingredient bestaat al (case insensitive match)"})

    def save(self, *args, **kwargs):
        self.full_clean()  # roept clean() aan, zorgt dat validatie gebeurt voor opslaan
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['ingredient']

def ingredienten_verwijderen(request):
    from recepten.forms import VerwijderHoofdIngredientForm
    if request.method == 'POST':
        form = VerwijderHoofdIngredientForm(request.POST)
        if form.is_valid():
            geselecteerde_ingredienten = form.cleaned_data['ingredienten']
            for ig in geselecteerde_ingredienten:
                try:
                    ig.delete()
                    messages.success(request, f"Ingredient '{ig}' is verwijderd.")
                except ProtectedError:
                    messages.error(
                        request,
                        f"Ingredient '{ig}' kan niet worden verwijderd omdat het nog gekoppeld is aan één of meer recepten."
                    )
            return redirect('catalog:ingredientlijst')
    else:
        form = VerwijderHoofdIngredientForm()
    return render(request, 'catalog/ingredienten_verwijderen.html', {'form': form})

def IngredientLijst(request):
    mijn_ingredienten = HoofdIngredienten.objects.all().values()
    template = loader.get_template("catalog/ingredient_lijst.html")
    context = {
            "mijn_ingredienten" : mijn_ingredienten
            }
    return HttpResponse(template.render(context, request))

def InvoerIngredient(request):
    template = loader.get_template("catalog/toevoegen_ingredient.html")
    return HttpResponse(template.render({},request))


def ToevoegenIngredient(request):
    ingredientnaam = request.POST['ingredient']
    nieuwe_ingredient = HoofdIngredienten(ingredient=ingredientnaam)
    ingredient_exists = HoofdIngredienten.objects.filter(ingredient__iexact=nieuwe_ingredient)
    if ingredient_exists.exists():
        return HttpResponseRedirect(reverse('catalog:ingredientlijst'))
    else:
        nieuwe_ingredient.save()
        return HttpResponseRedirect(reverse('catalog:ingredientlijst'))


