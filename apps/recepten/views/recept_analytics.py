# apps/recepten/views/recept_analytics.py

from django.views.generic import DetailView
from django.db.models import F
from apps.recepten.models import Recept
from apps.analytics.models import ReceptViewCount

class ReceptDetailView(DetailView):
    model = Recept
    template_name = "recepten/recept_detail.html"
    context_object_name = "recept"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        recept = self.object  # object is nu gegarandeerd geladen

        view_count, created = ReceptViewCount.objects.get_or_create(
            recept=recept,
            defaults={"count": 0}
        )

        view_count.count = F("count") + 1
        view_count.save(update_fields=["count"])
        view_count.refresh_from_db()  # F-expressie doorvoeren

        return response

