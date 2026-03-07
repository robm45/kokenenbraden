# views.py
from django.http import JsonResponse
from django.utils.timezone import now
from apps.analytics.models import DailyVisit, UserAgentLog

def track_visit(request):
    if request.method != "POST":
        return JsonResponse({"status": "ignored"}, status=400)

    user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
    ip = request.META.get("REMOTE_ADDR")

    UserAgentLog.objects.create(
        user_agent=user_agent,
        ip_address=ip
    )

    if not request.session.session_key:
        request.session.create()

    today = now().date()
    session_key = f"visited_{today}"

    if not request.session.get(session_key):
        visit, _ = DailyVisit.objects.get_or_create(date=today)
        visit.count += 1
        visit.save(update_fields=["count"])
        request.session[session_key] = True

    return JsonResponse({"status": "ok"})
