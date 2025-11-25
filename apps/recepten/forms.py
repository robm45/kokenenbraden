from django import forms
from .models import Categorie, GerechtType, HoofdIngredienten
from .models import Recept

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ["naam"] 


class GerechtTypeForm(forms.ModelForm):
    class Meta:
        model = GerechtType
        fields = ["gerecht_type"]   


class IngredientForm(forms.ModelForm):
    class Meta:
        model = HoofdIngredienten
        fields = ["ingredient"]   


class ReceptForm(forms.ModelForm):
    class Meta:
        model = Recept
        fields = "__all__"   # alle velden, inclusief 'foto'
        widgets = {
            "naam": forms.TextInput(attrs={"class": "form-control"}),
            "mapnummer": forms.TextInput(attrs={"class": "form-control"}),
            "samenvatting": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "bereidingstijd": forms.NumberInput(attrs={"class": "form-control"}),
            "aantal_personen": forms.TextInput(attrs={"class": "form-control"}),
            "bereiding": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "ingredienten": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "per_portie": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "hoofd_ingredienten": forms.SelectMultiple(attrs={"class": "form-select"}),
            "categorie": forms.Select(attrs={"class": "form-select"}),
            "gerecht_type": forms.Select(attrs={"class": "form-select"}),
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),  # 👈 nieuwe widget
        }

class ReceptZoekForm(forms.Form):
    zoekterm = forms.CharField(
        required=False,
        label="Zoekterm",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zoek in naam, ingrediënten of bereiding"})
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        label="Categorie",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    gerecht_type = forms.ModelChoiceField(
        queryset=GerechtType.objects.all(),
        required=False,
        label="Gerecht type",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    hoofd_ingredienten = forms.ModelMultipleChoiceField(
        queryset=HoofdIngredienten.objects.all(),
        required=False,
        label="Hoofdingrediënten",
        widget=forms.SelectMultiple(attrs={"class": "form-select"})
    )
    bereiding_filter = forms.ChoiceField(
        required = False,
        choices=[
            ('', '--- Bereidingstijd ---'),
            ('lt30', 'Minder dan 30 minuten'),
            ('30or60', 'Tussen 30 en 60 minuten'),
            ('gt60', 'Meer dan 60 minuten'),
        ]
    )

