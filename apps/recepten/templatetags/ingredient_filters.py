# recepten/templatetags/ingredient_filters.py

from django import template

register = template.Library()

FRACTIONS = {
    0.25: "¼",
    0.5: "½",
    0.75: "¾",
}

@register.filter
def format_hoeveelheid(ingredient):
    amount = ingredient.hoeveelheid
    unit = ingredient.eenheid

    # Stuks / geen eenheid → hele getallen
    if unit in ("", "st"):
        return str(int(round(amount)))

    integer = int(amount)
    fraction = round(amount - integer, 2)

    # Mooie breuken
    if fraction in FRACTIONS:
        if integer == 0:
            return FRACTIONS[fraction]
        return f"{integer}{FRACTIONS[fraction]}"

    # Overig: max 1 decimaal, geen .0
    if amount.is_integer():
        return str(int(amount))

    return str(round(amount, 1))

