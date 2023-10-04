# Import Django modules
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Import my_mfa modules
from .forms import RegistrationForm
from .models import UserProfile  

# Create your views here.

# Registration view function
def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST) # creates an instance of a RegistrationForm
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after registration
            return redirect("mfa") # Redirect to the mfa url
    else:
        form = RegistrationForm()  # IF request is not POST create an instance of the RegistrationForm without any data.
    return render(request, "registration/register.html", {"form": form})


# Defind a view for enabeling MFA
@login_required # Use the login_required decorator to ensure only authenticated users can access this view
def enable_mfa(request):
    try:
        # Retrieve user UserProfile details and if none is found, creates a new one.
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == "POST":
            # Enable MFA for the user
            user_profile.mfa_enabled = True
            user_profile.save()
            return redirect("mfa-method") # Redirect to the mfa-method url
        # Render the MFA enable form
        return render(request, "registration/enable_mfa.html", {"user_profile": user_profile, "created": created})
    except UserProfile.DoesNotExist:
        # Handle the case where UserProfile does not exist for the user
        return render(request, "registration/user_profile_not_found.html")


# Defind view for setting MFA method
@login_required
def set_mfa_method(request):
    # Retrieve user UserProfile details
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        # Get the value of the "mfa_method" field from the POST data.
        set_method = request.POST.get("mfa_method")
        # Update the user's MFA method in the UserProfile.
        user_profile.mfa_method = set_method
        user_profile.save()
        return render(request, "registration/mfa_success.html")
    return render(request, "registration/set_mfa_method.html", {"user_profile": user_profile})


# Defind a view for user authentication
def user_authentication(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user using their username and password
        user = authenticate(request, username=username, password=password)

        if user is not None: # If authentication is succesfull
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.mfa_enabled: # Check if mfa is enable for user
                if user_profile.mfa_method == "TOTP":
                    if not user_profile.secret_key: # If the UserProfile secret_key field is empty
                        return HttpResponse("Good TOTP")
                    else:
                        pass
                elif user_profile.mfa_method == "SMS":
                    if not user_profile.phone_number: # If the UserProfile phone_number field is empty
                        return HttpResponse("Good SMS")
                    else:
                        pass
                else:
                    messages.error(request, 'Invalid MFA method.')
                    return HttpResponse("I dont know yet")
            else:
                # MFA is not enabled, log the user in
                login(request, user)
                return HttpResponse("WELCOME TO 909INE")
        else:
            # Authentication failed, show an error message
            messages.error(request, 'Invalid username or password.')
    return render(request, "authentication/login.html") 


# Define a view for updating user MFA status
@login_required 
def update_mfa_status(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            user_profile.mfa_enabled = not user_profile.mfa_enabled # Toggle the MFA status
            user_profile.save()
            return HttpResponse("Successfull")
        except UserProfile.DoesNotExist:
            return render(request, "registration/user_profile_not_found.html") 
    return render(request, "registration/update_mfa_status.html", {"user_profile": user_profile})

