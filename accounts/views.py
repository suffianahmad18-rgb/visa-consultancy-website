# accounts/views.py - Replace your register function with this

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ClientProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import ClientProfile


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user normally

            # Check if profile exists (in case signal didn't create it)
            if not hasattr(user, "client_profile"):
                ClientProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data.get("phone", ""),
                    address=form.cleaned_data.get("address", ""),
                    country=form.cleaned_data.get("country", ""),
                )

            messages.success(request, f"Account created! You can now log in.")
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ClientProfileUpdateForm(request.POST, request.FILES, instance=request.user.client_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ClientProfileUpdateForm(instance=request.user.client_profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "accounts/profile.html", context)


def custom_logout(request):
    logout(request)
    return redirect("core:home")
