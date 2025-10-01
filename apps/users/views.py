from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import beheer_required

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
