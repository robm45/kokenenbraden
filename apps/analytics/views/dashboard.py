from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from user_agents import parse

from apps.analytics.models import ReceptViewCount, DailyVisit, UserAgentLog
from apps.recepten.models import Recept
from django.db.models import Sum, Count


class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def test_func(self):
        return self.request.user.groups.filter(name="beheer").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # totaal bezoekers
        context["total_visits"] = (
            DailyVisit.objects.aggregate(total=Sum("count"))["total"] or 0
        )

        # meest bezochte recepten
        context["top_recepten"] = (
            ReceptViewCount.objects
            .select_related("recept")
            .order_by("-count")[:10]
        )



        # recente user agents
        user_agents = UserAgentLog.objects.order_by("-created_at")[:100]

        context["user_agents"] = user_agents

        context["user_agents"] = (
            UserAgentLog.objects
            .order_by("-created_at")[:10]
        )

        # top user agents
        context["top_user_agents"] = (
            UserAgentLog.objects
             .values("user_agent")
             .annotate(count=Count("id"))
             .order_by("-count")[:10]
        )

        # bots vs browsers
        bots = 0
        browsers = 0

        for log in user_agents:
            ua = parse(log.user_agent)
            if ua.is_bot:
                bots += 1
            else:
                browsers += 1

        context["bot_count"] = bots
        context["browser_count"] = browsers


        return context

