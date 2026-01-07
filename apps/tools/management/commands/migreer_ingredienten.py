# apps/tools/management/commands/migreer_ingredienten.py
from django.core.management.base import BaseCommand
from apps.recepten.models import Recept, Ingredient
from fractions import Fraction
import re

# DRY_RUN = True → alleen printen, geen data opslaan
DRY_RUN = False

# Mapping van eenheden
EENHEDEN_MAP = {
    "gr": "gr",
    "gram": "gr",
    "g": "gr",
    "kg": "kg",
    "ml": "ml",
    "l": "l",
    "el": "el",
    "eetlepel": "el",
    "tl": "tl",
    "theelepel": "tl",
    "stuk": "st",
    "stuks": "st",
    "teentje": "st",
    "bosje": "st",
}

STUK_WOORDEN = [
    "ui", "uien",
    "teentje", "teentjes",
    "teen", "tenen",
    "paprika", "paprika’s", "paprika's",
    "blokje", "blokjes",
    "stuk", "stukken",
    "bosje", "bosjes",
    "tomaten", "tomaten",
]

UNICODE_FRACTIONS = {
    "½": "1/2",
    "¼": "1/4",
    "¾": "3/4",
    "⅓": "1/3",
    "⅔": "2/3",
}

def normalize_regel(regel):
    regel = regel.strip()

    # evt., eventueel verwijderen
    regel = re.sub(r"^(evt\.?|eventueel)\s*", "", regel, flags=re.I)

    # 1½ → 1 ½
    regel = re.sub(r"(\d)([¼½¾⅓⅔])", r"\1 \2", regel)

    # unicode breuken → ascii
    for char, frac in UNICODE_FRACTIONS.items():
        regel = regel.replace(char, frac)

    return regel

def parse_hoeveelheid(qty_raw):
    if not qty_raw:
        return 1

    # 1 1/2
    if " " in qty_raw and "/" in qty_raw:
        whole, frac = qty_raw.split()
        return int(whole) + float(Fraction(frac))

    # 1/2
    if "/" in qty_raw:
        return float(Fraction(qty_raw))

    # 2-3 → 3
    if "-" in qty_raw:
        return int(qty_raw.split("-")[-1])

    return int(qty_raw)


def parse_ingredient_regel(regel):
    regel = normalize_regel(regel)

    if not re.match(r"^\d", regel):
        return 1, "-", regel

    match = re.match(r"^(?P<qty>\d+(?: \d+/\d+)?|\d+/\d+|\d+-\d+)\s+(?P<rest>.+)$", regel)
    if not match:
        return 1, "-", regel

    qty_raw = match.group("qty")
    rest = match.group("rest").strip()

    hoeveelheid = parse_hoeveelheid(qty_raw)
    eenheid = "-"
    naam = rest

    # bekende eenheden
    for key, val in EENHEDEN_MAP.items():
        if rest.lower().startswith(key + " "):
            eenheid = val
            naam = rest[len(key):].strip()
            break

    # stuk-woorden
    for woord in STUK_WOORDEN:
        if rest.lower().startswith(woord):
            eenheid = "st"
            naam = rest
            break

    naam = re.sub(r"'s\b", "", naam)
    naam = naam.strip(" -+")

    return hoeveelheid, eenheid, naam


class Command(BaseCommand):
    help = "Migreer ingredienten tekstveld naar Ingredient model"

    def handle(self, *args, **options):
        recepten = Recept.objects.exclude(ingredienten="").order_by("id")
        for recept in recepten:
            regels = recept.ingredienten.splitlines()
            for regel in regels:
                hoeveelheid, eenheid, naam = parse_ingredient_regel(regel)

                # DRY_RUN → printen
                if DRY_RUN:
                    self.stdout.write(
                        f"[DRY-RUN] Recept: {recept.naam} | "
                        f" {regel} -->  "
                        f" {hoeveelheid} | "
                        f" {eenheid} | "
                        f" {naam}"
                    )
                else:
                    # echte create
                    Ingredient.objects.create(
                        recept=recept,
                        ingredient_naam=naam,
                        hoeveelheid=hoeveelheid,
                        eenheid=eenheid
                    )
            self.stdout.write(f"✔ {recept.naam} gemigreerd")

