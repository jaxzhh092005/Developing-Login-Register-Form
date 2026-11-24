from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

from .forms import RegisterForm

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)          # AUTHENTICATION: start a session
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})


@login_required                        # AUTHENTICATION gate: must be logged in
def home(request):
    return render(request, "accounts/home.html")


@login_required
@permission_required("accounts.view_all_profiles", raise_exception=True)   # AUTHORIZATION gate: must have permission, else 403
def member_list(request):
    users = User.objects.select_related("profile").prefetch_related("groups").order_by("first_name")
    return render(request, "accounts/members.html", {"members": users})
