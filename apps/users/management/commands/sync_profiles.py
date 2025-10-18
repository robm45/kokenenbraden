from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import UserProfile

class Command(BaseCommand):
    help = "Synchroniseert UserProfile records voor alle gebruikers zonder profiel."

    def handle(self, *args, **options):
        created_count = 0
        total_users = User.objects.count()

        for user in User.objects.all():
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Nieuw profiel aangemaakt voor: {user.username}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Synchronisatie voltooid: {created_count} nieuw(e) profiel(en) op {total_users} gebruikers."
            )
        )

