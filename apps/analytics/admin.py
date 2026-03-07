from django.contrib import admin
from .models import DailyVisit
from .models import ReceptViewCount
from .models import UserAgentLog
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages


@admin.register(DailyVisit)
class DailyVisitAdmin(admin.ModelAdmin):
    list_display = ("date", "count")
    ordering = ("-date",)
    change_list_template = "admin/analytics/reset_analytics_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "reset-analytics/",
                self.admin_site.admin_view(self.reset_analytics),
                name="reset-analytics",
            ),
        ]
        return custom_urls + urls

    def reset_analytics(self, request):
        if request.method == "POST":
            DailyVisit.objects.all().delete()
            ReceptViewCount.objects.all().delete()

            self.message_user(
                request,
                "Analytics zijn succesvol gereset.",
                messages.SUCCESS,
            )
            return redirect("..")

        return render(
            request,
            "admin/analytics/reset_analytics_confirm.html",
        )

@admin.register(ReceptViewCount)
class ReceptViewCountAdmin1(admin.ModelAdmin):
    list_display = ("recept", "count")
    ordering = ("-count",)


@admin.register(UserAgentLog)
class UserAgentLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "ip_address", "user_agent")
    search_fields = ("user_agent",)
