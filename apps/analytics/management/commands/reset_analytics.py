from django.core.management.base import BaseCommand
from apps.analytics.models import DailyVisit, ReceptViewCount


class Command(BaseCommand):
    help = "Reset analytics data (daily visits en/of recept view counts)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--daily",
            action="store_true",
            help="Reset alleen DailyVisit data",
        )
        parser.add_argument(
            "--recepten",
            action="store_true",
            help="Reset alleen ReceptViewCount data",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Reset alle analytics data",
        )

    def handle(self, *args, **options):
        if not (options["daily"] or options["recepten"] or options["all"]):
            self.stdout.write(
                self.style.WARNING(
                    "Geen optie opgegeven. Gebruik --daily, --recepten of --all"
                )
            )
            return

        if options["daily"] or options["all"]:
            deleted, _ = DailyVisit.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"DailyVisit records verwijderd: {deleted}")
            )

        if options["recepten"] or options["all"]:
            deleted, _ = ReceptViewCount.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"ReceptViewCount records verwijderd: {deleted}")
            )

        self.stdout.write(self.style.SUCCESS("Analytics reset voltooid."))

