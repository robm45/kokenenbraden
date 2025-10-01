from django.urls import path
from . import views

app_name = 'recepten'

urlpatterns = [
    path("", views.welkom, name="welkom"),
    path("lijst/", views.recept_lijst, name="recept_lijst"),
    # Recept beheer
    path("invoer/", views.recept_invoer, name="recept_invoer"),
    path("delete/<int:pk>/", views.recept_delete, name="recept_delete"),
    path("bewerk/<int:pk>/", views.recept_bewerk, name="recept_bewerk"),
    path("detail/<int:pk>/", views.recept_detail, name="recept_detail"),


    # categorie
    path("categorie/", views.categorie_lijst, name="categorie_lijst"),
    path("categorie/invoer/", views.categorie_invoer, name="categorie_invoer"),
    path("categorie/delete/<int:pk>/", views.categorie_delete, name="categorie_delete"),

    # gerecht type
    path("gerecht_type/invoer/", views.gerecht_type_invoer, name="gerecht_type_invoer"),
    path("gerecht_type/lijst/", views.gerecht_type_lijst, name="gerecht_type_lijst"),
    path("gerecht_type/delete/<int:pk>/", views.gerecht_type_delete, name="gerecht_type_delete"),

    # ingredient
    path("ingredient/invoer/", views.ingredient_invoer, name="ingredient_invoer"),
    path("ingredient/lijst/", views.ingredient_lijst, name="ingredient_lijst"),
    path("ingredient/delete/<int:pk>/", views.ingredient_delete, name="ingredient_delete"),
    
    # zoekfunctie
    path("zoeken/", views.recept_zoek, name="recept_zoek"),

    # print naar pdf
    path("recept/<int:pk>/export_pdf", views.export_recept_pdf, name="recept-export-pdf")
]
