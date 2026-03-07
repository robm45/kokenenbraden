from django.contrib import admin
from .models import Categorie, GerechtType, HoofdIngredienten, Recept, Ingredient

# Registreren van modellen bij de admin
admin.site.register(Categorie)
admin.site.register(GerechtType)
#admin.site.register(HoofdIngredienten)
admin.site.register(Ingredient)

class IngredientenInline(admin.TabularInline):
    model = Ingredient
    extra = 0
    fields = ( 'ingredient_naam', 'hoeveelheid', 'eenheid')


class ReceptAdmin(admin.ModelAdmin):
    fieldsets = (
    (None, {
        'fields': ('naam', 'mapnummer', 'categorie', 'bereidingstijd', 'aantal_personen', 'gerecht_type', 'ingredienten', 'foto')
    }),
    )
    
    readonly_fields = ('ingredienten',)

    inlines = [IngredientenInline]


admin.site.register(Recept, ReceptAdmin)
