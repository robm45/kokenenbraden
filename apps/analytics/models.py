from django.db import models
from apps.recepten.models import Recept
from django.utils.timezone import now

class DailyVisit(models.Model):
    date = models.DateField(unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} – {self.count}"

class ReceptViewCount(models.Model):
    recept = models.OneToOneField(
        "recepten.Recept",
        on_delete=models.CASCADE,
        related_name="view_count"
    )
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.recept.naam}: {self.count}"


class UserAgentLog(models.Model):
    created_at = models.DateTimeField(default=now)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.user_agent[:80]
