from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from reviews.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("reviews:home")  # Redirect to the profile view
        
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def create_profile_view(request):
    if request.method == "POST":
        bio = request.POST.get("bio")
        reading_goal = request.POST.get("reading_goal")
        profile_picture = request.FILES.get("profile_picture")

        # Check if the user already has a profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Update fields
        if bio:
            user_profile.bio = bio
        if reading_goal:
            user_profile.reading_goal = int(reading_goal)
        if profile_picture:
            user_profile.profile_picture = profile_picture
        user_profile.save()

        return redirect("profile")  # Redirect to the profile page

    return render(request, "accounts/create_profile.html")
