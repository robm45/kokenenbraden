from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
from django.shortcuts import get_object_or_404
import os
import math

from ..models.recept import *  # pas aan naar jouw app/model

def format_hoeveelheid(amount, unit):

    if amount is None  or amount == 0:
        print("   ➜ Geen hoeveelheid → lege string")
        return ""

    # stuks afronden
    if unit == "st":
        return str(round(amount))

    whole = int(amount)
    fraction = amount - whole

    fractions = [
        (0.75, "¾"),
        (0.66, "⅔"),
        (0.5,  "½"),
        (0.33, "⅓"),
        (0.25, "¼"),
    ]

    frac_symbol = ""
    for value, symbol in fractions:
        if abs(fraction - value) < 0.08:
            frac_symbol = symbol
            break

    if whole == 0 and frac_symbol:
        return frac_symbol
    if whole > 0 and frac_symbol:
        return f"{whole}{frac_symbol}"

    # fallback: 1 decimaal, NL-notatie
    if float(amount).is_integer():
        return str(int(amount))

    return f"{amount:.1f}".replace(".", ",")


def export_recept_pdf(request, pk):
    recept = get_object_or_404(Recept, pk=pk)

    gekozen_personen = int(request.GET.get("personen", recept.aantal_personen))
    basis_personen = int(recept.aantal_personen)
    factor = gekozen_personen / basis_personen if basis_personen else 1

    ingredienten = []
    for item in recept.ingredient_items.all():

        if item.schaling == "none" or item.hoeveelheid == 0:
            hoeveelheid = None
            print("   ➜ Geen schaling / geen hoeveelheid")
        elif item.schaling == "fixed":
            hoeveelheid = item.hoeveelheid
            print("   ➜ Fixed hoeveelheid:", hoeveelheid)
        else:
            hoeveelheid = item.hoeveelheid * factor
            print("   ➜ Geschaald:", hoeveelheid)

        if item.eenheid == "st" and hoeveelheid is not None:
            hoeveelheid = math.ceil(hoeveelheid)
            print("   ➜ Afgerond (st):", hoeveelheid)

        hoeveelheid_str = format_hoeveelheid(hoeveelheid, item.eenheid)

        print("   ✔ Eindresultaat:", hoeveelheid_str)

        ingredienten.append({
            "naam": item.ingredient_naam,
            "hoeveelheid": hoeveelheid_str,
            "eenheid": item.eenheid or ""
        })


    if recept.foto:
        foto_pad = 'file://' + os.path.join(settings.MEDIA_ROOT, recept.foto.name)
    else:
        foto_pad = None

    html_string = render_to_string(
        'recepten/recept_pdf.html',
        {
            'recept': recept,
            'ingredienten': ingredienten,
            'personen': gekozen_personen,
            'foto_pad': foto_pad
        }
    )

    css_file = os.path.join(settings.BASE_DIR, 'static', 'css', 'pdf.css')
    css = CSS(filename=css_file)

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recept.naam}.pdf"'
    return response

