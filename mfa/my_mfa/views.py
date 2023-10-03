from django.contrib.auth import login
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegistrationForm
from .models import UserProfile  

# Create your views here.

# Registration view function
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after registration
            return redirect("mfa")
    else:
        form = RegistrationForm()  
    return render(request, "registration/register.html", {"form": form})



# Defind a view for enabeling MFA
@login_required # Use the login_required decorator to ensure only authenticated users can access this view
def enable_mfa(request):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            # Enable MFA for the user
            user_profile.mfa_enabled = True
            user_profile.save()
            return redirect("mfa-method")
        # Render the MFA enable form
        return render(request, "registration/enable_mfa.html", {"user_profile": user_profile, "created": created})
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile does not exist for the user
        return render(request, "registration/user_profile_not_found.html")


# Defind view for setting MFA method
@login_required
def set_mfa_method(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        set_method = request.POST.get("mfa_method")
        user_profile.mfa_method = set_method

        # if set_method == "SMS":
        #     user_profile.mfa_method = set_method
        #     user_profile.phone_number = request.POST.get("phone_number")
        # elif set_method == "TOTP":
        #     pass
        user_profile.save()
        return HttpResponse(f"Your preferd MFA method is {set_method}")
    return render(request, 'registration/set_mfa_method.html', {'user_profile': user_profile})


# Define a view for updating user MFA status
@login_required 
def update_mfa_status(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            user_profile.mfa_enabled = not user_profile.mfa_enabled # Toggle the MFA status
            user_profile.save()
            return HttpResponse("Successfull")
        except UserProfile.DoesNotExist:
            return render(request, 'registration/user_profile_not_found.html') 
    return render(request, "registration/update_mfa_status.html", {'user_profile': user_profile})

    


def user_authentication(request):
    pass



def mfa_verification(request):
    pass