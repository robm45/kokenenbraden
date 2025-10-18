from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import beheer_required
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@beheer_required
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        groups = request.POST.getlist("groups")
        if form.is_valid():
            user = form.save()
            if groups:
                user.groups.set(Group.objects.filter(id__in=groups))
            messages.success(request, f"Gebruiker {user.username} is aangemaakt.")
            return redirect("users:create_user")
    else:
        form = UserCreationForm()
    all_groups = Group.objects.all()
    return render(request, "users/create_user.html", {"form": form, "groups": all_groups})


@login_required
def preferences(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        wants_mail = "receive_monthly_mail" in request.POST
        profile.receive_monthly_mail = "receive_monthly_mail" in request.POST
        profile.save()

        if wants_mail:
            messages.success(request, "Je bent ingeschreven voor maandelijks receptenrapport.")
        else:

            messages.info(request, "Je bent uitgeschreven voor maandelijks receptenrapport.")
        return redirect("recepten:welkom")

    return render(request, "users/preferences.html", {"profile": profile})

