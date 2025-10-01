from django.contrib import admin
from .models import Categorie, GerechtType, HoofdIngredienten, Recept

# Registreren van modellen bij de admin
admin.site.register(Categorie)
admin.site.register(GerechtType)
admin.site.register(HoofdIngredienten)
#admin.site.register(Recept)

class ReceptAdmin(admin.ModelAdmin):
    list_display = ('mapnummer','naam', 'categorie', 'bereidingstijd', 'aantal_personen', 'gerecht_type')

admin.site.register(Recept, ReceptAdmin)