import os
from django.db import models
from PIL import Image
from django.urls import reverse
from .categorie import Categorie
from .ingredient import HoofdIngredienten
from .gerechttype import GerechtType
from apps.recepten.utils import recept_image_path


class Recept(models.Model):
    mapnummer = models.CharField(max_length=10, blank=True)
    naam = models.CharField(max_length=200)
    samenvatting = models.TextField(max_length=100, blank=True, null=True)
    bereidingstijd = models.IntegerField(default=30)
    aantal_personen = models.CharField(default=4, max_length=10)
    bereiding = models.TextField(max_length=2500)
    ingredienten = models.TextField(max_length=1000)
    hoofd_ingredienten = models.ManyToManyField(HoofdIngredienten)
    categorie = models.ForeignKey(Categorie, on_delete=models.RESTRICT, null=True)
    gerecht_type = models.ForeignKey(GerechtType, on_delete=models.RESTRICT, null=True)
    per_portie = models.TextField(max_length=1000)
    foto = models.ImageField(upload_to=recept_image_path, blank=True, null=True)

    def __str__(self):
        return self.naam

    def get_absolute_url(self):
        return reverse('catalog:recept-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.foto:
            img_path = self.foto.path
            with Image.open(img_path) as img:
                img.thumbnail((810, 650))
                img.save(img_path)




