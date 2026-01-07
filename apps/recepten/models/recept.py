import os
from django.db import models
from PIL import Image
from django.urls import reverse
from .categorie import Categorie
from .ingredient import HoofdIngredienten
from .gerechttype import GerechtType
from apps.recepten.utils import recept_image_path

# Reccept model
class Recept(models.Model):
    mapnummer = models.CharField(max_length=10, blank=True)
    naam = models.CharField(max_length=200)
    samenvatting = models.TextField(max_length=100, blank=True, null=True)
    bereidingstijd = models.IntegerField(default=30)
    aantal_personen = models.PositiveIntegerField(default=4)
    bereiding = models.TextField(max_length=2500)
    ingredienten = models.TextField(max_length=1000, blank=True, null=True)
    hoofd_ingredienten = models.ManyToManyField(HoofdIngredienten)
    categorie = models.ForeignKey(Categorie, on_delete=models.RESTRICT, null=True)
    gerecht_type = models.ForeignKey(GerechtType, on_delete=models.RESTRICT, null=True)
    per_portie = models.TextField(max_length=1000)
    datum_toegevoegd = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to=recept_image_path, blank=True, null=True)

    def __str__(self):
        return self.naam

    def get_absolute_url(self):
        return reverse('recepten:recept_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            img_path = self.foto.path
            with Image.open(img_path) as img:
                img.thumbnail((810, 650))
                img.save(img_path)

# Ingredienten basis 4 personen
class Ingredient(models.Model):

    EENHEID_CHOICES = [
        ("", "-"),
        ("gr", "gram"),
        ("kg", "kilogram"),
        ("ml", "milliliter"),
        ("l", "liter"),
        ("el", "eetlepel"),
        ("tl", "theelepel"),
        ("st", "stuk"),
    ]

    recept = models.ForeignKey(Recept, related_name='ingredient_items', on_delete=models.CASCADE)
    ingredient_naam=models.CharField(max_length=100)
    hoeveelheid = models.FloatField()
    eenheid = models.CharField(max_length=5, choices=EENHEID_CHOICES, blank=True)

    def __str__(self):
        if self.eenheid:
            return f"{self.hoeveelheid} {self.get_eenheid_display()} {self.ingredient_naam} ({self.recept.naam})"
        return f"{self.hoeveelheid} {self.ingredient_naam} ({self.recept.naam})"

