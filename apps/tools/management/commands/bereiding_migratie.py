import re
from django.core.management.base import BaseCommand
from apps.recepten.models import Recept  # pas aan!


def convert_bereiding_to_html(text):
    if not text:
        return ""

    lines = text.splitlines()
    html = []
    in_list = False
    current_li = None

    for line in lines:
        line = line.strip()

        if not line:
            if current_li is not None:
                if not current_li or not current_li[-1].endswith("<br>"):
                    current_li.append("<br>")
            continue

        match = re.match(r"^\d+\.\s*(.*)", line)

        if match:
            if not in_list:
                html.append("<ol>")
                in_list = True

            if current_li is not None:
                html.append(f"<li>{''.join(current_li)}</li>")

            current_li = [match.group(1)]

        else:
            if current_li is not None:
                current_li.append("<br>" + line)
            else:
                if in_list:
                    html.append("</ol>")
                    in_list = False
                html.append(f"<p>{line}</p>")

    if current_li is not None:
        html.append(f"<li>{''.join(current_li)}</li>")

    if in_list:
        html.append("</ol>")

    return "".join(html)


class Command(BaseCommand):
    help = "Preview or migrate 'bereiding' field to HTML"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Write output to /tmp instead of saving",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        output_file = "/tmp/bereiding_migratie.txt"

        changed = 0

        if dry_run:
            f = open(output_file, "w", encoding="utf-8")

        for obj in Recept.objects.all():
            old_text = obj.bereiding or ""

            # skip als al HTML
            if "<p>" in old_text or "<ol>" in old_text:
                continue

            new_text = convert_bereiding_to_html(old_text)

            if old_text == new_text:
                continue

            changed += 1

            if dry_run:
                f.write("=" * 80 + "\n")
                f.write(f"ID: {obj.id}\n\n")
                f.write("OUDE TEKST:\n")
                f.write(old_text + "\n\n")
                f.write("NIEUWE HTML:\n")
                f.write(new_text + "\n\n")
            else:
                obj.bereiding = new_text
                obj.save(update_fields=["bereiding"])

        if dry_run:
            f.write(f"\nTOTAAL GEWIJZIGD: {changed}\n")
            f.close()
            self.stdout.write(self.style.SUCCESS(f"Preview geschreven naar {output_file}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"{changed} records gemigreerd"))