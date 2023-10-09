# Import Django modules
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Import third party modules
# from qrcode.image.pure import PymagingImage
from PIL import Image as PilImage
import pyotp
import qrcode
import io
from django.core.files.base import ContentFile

# Import my_mfa modules
from .forms import RegistrationForm
from .models import UserProfile 
from .utils import *  

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
                    if not user_profile.totp_secret_key: # If the UserProfile secret_key field is empty
                        return redirect("totp-qr-code")
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


# Defind a view to generate totp_qr_code
@login_required
def generate_totp_qr_code(request):
    # Generate secret key in base32 format
    secret_key = generate_key()
    print(secret_key)
    encryption_key = generate_encryption_key() # Generate encryption key
    print(encryption_key)
    encrypt_secret_key = encrypt_secret(secret_key, encryption_key) # Encrypt totp_secret_key

    # Retrieve user UserProfile details
    user_profile = UserProfile.objects.get(user=request.user)
    username = user_profile.user.username # Get user name from django in-built User models

    # Update UserProfile details
    user_profile.encryption_key = encryption_key
    user_profile.totp_secret_key = encrypt_secret_key
    user_profile.save()
    print(user_profile.encryption_key)
    print(user_profile.totp_secret_key)
    
    # Create a TOTP object
    totp = pyotp.TOTP(secret_key)
    # Generate the current TOTP value
    totp_value = totp.now()
    # Create a TOTP provisioning URL
    totp_url = totp.provisioning_uri(username, issuer_name="909ine MFA System")
    # Generate a QR code for the TOTP URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        #image_factory=PilImage,
    )
    qr.add_data(totp_url)
    qr.make(fit=True)
    qr_code_image = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a specific format (e.g., PNG) using Pillow
    image_io = io.BytesIO()
    qr_code_image.save(image_io, format="PNG")
    image_io.seek(0)

    # Save the QR code image to the model
    user_profile.name = "QR Code"
    #user_profile.image.save("qr_code.png", qr_code_image)
    user_profile.image.save("qr_code.png", ContentFile(image_io.read()))

    qr_code = user_profile.image.url
    
    # Pass the TOTP URL, QR code image, secret key, and TOTP value to the template
    context = {
        "totp_url": totp_url,
        "qr_code": qr_code,
        "totp_value": totp_value,
        "username": username,
    }

    return render(request, "authentication/generate_totp.html",context)


# Defind view to verify totp
def verify_totp(request):
    if request.method == "POST":
        # Get the TOTP code entered by the user
        user_input_totp = request.POST.get("totp_code")

        # Get user's profile
        user_profile = UserProfile.objects.get(user=request.user)

        encryption_key = user_profile.encryption_key
        secret_key = user_profile.totp_secret_key
        decrypted_secret_key = decrypt_totp_secret_key(secret_key, encryption_key)
        print(encryption_key)
        print(secret_key)
        print(decrypted_secret_key)

        # Verify the TOTP code
        #totp = pyotp.TOTP(user_profile.totp_secret_key)
        totp = pyotp.TOTP(decrypted_secret_key)
        if totp.verify(user_input_totp):
            messages.success(request, "TOTP code is valid.")
        else:
            messages.error(request, "Invalid TOTP code.")
    return render(request, "authentication/verify_totp.html")


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

