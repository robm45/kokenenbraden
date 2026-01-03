from django.utils.timezone import now
from .models import DailyVisit, ReceptViewCount

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # sessie aanmaken
        if not request.session.session_key:
            request.session.create()

        today = now().date()
        session_key = f"visited_{today}"

        # DAGELIJKSE BEZOEKER
        if not request.session.get(session_key):
            visit, _ = DailyVisit.objects.get_or_create(date=today)
            visit.count += 1
            visit.save(update_fields=["count"])
            request.session[session_key] = True

        response = self.get_response(request)
        return response

