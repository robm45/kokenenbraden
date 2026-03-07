from django.urls import path
from .views.dashboard import AnalyticsDashboardView
from .views.tracking import track_visit

app_name = "analytics"

urlpatterns = [
    path("dashboard", AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
    path("track-visit/", track_visit, name="track_visit"),
]

