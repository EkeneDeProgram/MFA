# Import Django modules
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.http import JsonResponse

# Import third party modules
from PIL import Image as PilImage
import pyotp
import qrcode
import io

# Import my_mfa modules
from .forms import RegistrationForm
from .models import UserProfile 
from .utils import *  

# Create your views here.

def index(request):
    return render(request, "index.html")


# Defin Registration view
def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST) # creates an instance of a RegistrationForm
        if form.is_valid():
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            # Perform server-side email validation
            if not is_valid_email(email):
                form.add_error("email", "Invalid email address.")
            else:
                user = form.save()
                # Create a UserProfile instance and link it to the user
                user_profile = UserProfile(user=user)
                # Check if the "Enable MFA" checkbox is selected
                if request.POST.get("enable_mfa"):
                    user_profile.mfa_enabled = True
                    user_profile.save()
                login(request, user) # Automatically log the user in after registration
                return redirect("index")
    else:
        form = RegistrationForm()  # IF request is not POST create an instance of the RegistrationForm without any data.
    return render(request, "register.html", {"form": form})


# Defind a view for user authentication
@login_required
def user_authentication(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate the user using their username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                if not user_profile.totp_secret_key: # If the UserProfile secret_key field is empty
                    return redirect("totp-qr-code") # Redirect to totp-qr-code url
                else:
                    return redirect("verify-totp")
            except UserProfile.DoesNotExist:
                return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html") 


# Defind a view to generate totp qr code
@login_required
def generate_totp_qr_code(request):
    # Generate secret key in base32 format
    secret_key = pyotp.random_base32()
    # Specify the time step (in seconds)
    time_step = 30
    
    user = request.user  # Get the authenticated user
    # Retrieve user UserProfile details
    user_profile = UserProfile.objects.get(user=user)
    username = user_profile.user.username # Get user name from django in-built User models

    # Update UserProfile details
    user_profile.totp_secret_key = secret_key
    user_profile.save()
   
    # Create a TOTP object with the specified time step
    totp = pyotp.TOTP(user_profile.totp_secret_key, interval=time_step)
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
    
    # Pass the TOTP URL, QR code image, TOTP value and username to the template
    context = {
        "totp_url": totp_url,
        "qr_code": qr_code,
        "totp_value": totp_value,
        "username": username,
    }

    return render(request, "generate_totp.html",context)


# Defind view to verify totp code
@login_required
def verify_totp(request):
    if request.method == "POST":
        # Get the TOTP code entered by the user
        user_input_totp = request.POST.get("totp_code")

        # Get user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        # Verify the TOTP code
        totp = pyotp.TOTP(user_profile.totp_secret_key)
        if  totp.verify(user_input_totp):
            messages.success(request, "TOTP code is valid.")
            return render(request, "index.html")
        else:
           messages.error(request, "Invalid TOTP code.")  
    return render(request, "verify_totp.html")

